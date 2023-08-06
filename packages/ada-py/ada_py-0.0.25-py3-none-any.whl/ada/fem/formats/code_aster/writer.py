import logging
from itertools import chain
from typing import Iterable, Tuple, Union

import numpy as np

from ada.concepts.levels import Assembly, Part
from ada.concepts.points import Node
from ada.concepts.structural import Material
from ada.config import Settings as _Settings
from ada.fem import Bc, FemSection, StepEigen, StepImplicit
from ada.fem.containers import FemSections
from ada.fem.shapes import ElemShapeTypes
from ada.fem.utils import is_quad8_shell_elem, is_tri6_shell_elem

from ..utils import get_fem_model_from_assembly
from .common import abaqus_to_med_type
from .compatibility import check_compatibility
from .templates import el_convert_str, main_comm_str
from .write_loads import write_load


def to_fem(assembly: Assembly, name, analysis_dir, metadata=None):
    """Write Code_Aster .med and .comm file from Assembly data"""
    from ada.materials.utils import shorten_material_names

    check_compatibility(assembly)

    if "info" not in metadata:
        metadata["info"] = dict(description="")

    p = get_fem_model_from_assembly(assembly)
    # Prepare model for
    shorten_material_names(assembly)
    # TODO: Implement support for multiple parts. Need to understand how submeshes in Salome and Code Aster works.
    # for p in filter(lambda x: len(x.fem.elements) != 0, assembly.get_all_parts_in_assembly(True)):
    write_to_med(name, p, analysis_dir)

    with open((analysis_dir / name).with_suffix(".comm"), "w") as f:
        f.write(create_comm_str(assembly, p))

    print(f'Created a Code_Aster input deck at "{analysis_dir}"')


def create_comm_str(assembly: Assembly, part: Part) -> str:
    """Create COMM file input str"""
    all_mat = chain.from_iterable([p.materials for p in assembly.get_all_parts_in_assembly(True)])
    all_mat_unique = {x.name: x for x in all_mat}
    materials_str = "\n".join([write_material(mat) for mat in all_mat_unique.values()])
    sections_str = write_sections(part.fem.sections)
    bc_str = "\n".join([create_bc_str(bc) for bc in assembly.fem.bcs + part.fem.bcs])
    step_str = "\n".join([create_step_str(s, part) for s in assembly.fem.steps])

    type_tmpl_str = "_F(GROUP_MA={elset_str}, PHENOMENE='MECANIQUE', MODELISATION='{el_formula}',),"

    model_type_str = ""
    section_sets = ""
    input_mesh = "mesh"
    if len(part.fem.sections.lines) > 0:
        bm_elset_str = ",".join([f"'{bm_fs.elset.name}'" for bm_fs in part.fem.sections.lines])
        section_sets += f"bm_sets = ({bm_elset_str})\n"
        model_type_str += type_tmpl_str.format(elset_str="bm_sets", el_formula="POU_D_E")

    if len(part.fem.sections.shells) > 0:
        sh_elset_str = ""
        second_order = ""
        is_tri6 = False
        is_quad8 = False
        for sh_fs in part.fem.sections.shells:
            is_quad8 = is_quad8_shell_elem(sh_fs)
            is_tri6 = is_tri6_shell_elem(sh_fs)
            if is_tri6 or is_quad8:
                second_order += f"'{sh_fs.elset.name}',"
            else:
                sh_elset_str += f"'{sh_fs.elset.name}',"

        if sh_elset_str != "":
            elset = "sh_sets"
            section_sets += f"{elset} = ({sh_elset_str})\n"
            model_type_str += type_tmpl_str.format(elset_str=elset, el_formula="DKT")

        if second_order != "":
            elset = "sh_2nd_order_sets"
            section_sets += f"{elset} = ({second_order})\n"

            if is_tri6:
                output_mesh = "ma_tri6"
                section_sets += el_convert_str.format(
                    output_mesh=output_mesh, input_mesh=input_mesh, el_set=elset, convert_option="TRIA6_7"
                )
                input_mesh = output_mesh

            if is_quad8:
                output_mesh = "ma_quad8"
                section_sets += el_convert_str.format(
                    output_mesh=output_mesh, input_mesh=input_mesh, el_set=elset, convert_option="QUAD8_9"
                )
                input_mesh = output_mesh
            model_type_str += type_tmpl_str.format(elset_str=elset, el_formula="COQUE_3D")

    if len(part.fem.sections.solids) > 0:
        so_elset_str = ",".join([f"'{solid_fs.elset.name}'" for solid_fs in part.fem.sections.solids])
        section_sets += f"so_sets = ({so_elset_str})\n"
        model_type_str += type_tmpl_str.format(elset_str="so_sets", el_formula="3D")

    comm_str = main_comm_str.format(
        section_sets=section_sets,
        input_mesh=input_mesh,
        model_type_str=model_type_str,
        materials_str=materials_str,
        sections_str=sections_str,
        bc_str=bc_str,
        step_str=step_str,
    )

    return comm_str


def write_to_med(name, part: Part, analysis_dir):
    """Custom Method for writing a part directly based on meshio"""
    import pathlib

    import h5py

    analysis_dir = pathlib.Path(analysis_dir)
    filename = (analysis_dir / name).with_suffix(".med")

    f = h5py.File(filename, "w")
    mesh_name = name if name is not None else part.fem.name
    # Strangely the version must be 3.0.x
    # Any version >= 3.1.0 will NOT work with SALOME 8.3
    info = f.create_group("INFOS_GENERALES")
    info.attrs.create("MAJ", 3)
    info.attrs.create("MIN", 0)
    info.attrs.create("REL", 0)

    time_step = _write_mesh_presets(f, mesh_name)

    profile = "MED_NO_PROFILE_INTERNAL"

    # Node and Element sets (familles in French)
    fas = f.create_group("FAS")
    families = fas.create_group(mesh_name)
    family_zero = families.create_group("FAMILLE_ZERO")  # must be defined in any case
    family_zero.attrs.create("NUM", 0)

    # Make sure that all member references are updated (TODO: Evaluate if this can be avoided using a smarter algorithm)
    part.fem.sets.add_references()

    # Nodes and node sets
    _write_nodes(part, time_step, profile, families)

    # Elements (mailles in French) and element sets
    _write_elements(part, time_step, profile, families)

    f.close()


def write_material(material: Material) -> str:
    from ada.core.utils import NewLine

    # Bi-linear hardening ECRO_LINE=_F(D_SIGM_EPSI=2.0e06, SY=2.35e06,)

    model = material.model
    nl = NewLine(3, suffix="	")

    if model.plasticity_model is not None:
        nl_mat = "nl_mat=(	\n	"
        eps = [e for e in model.eps_p]
        eps[0] = 1e-5  # Epsilon index=0 cannot be zero
        nl_mat += "".join([f"{e:.4E},{s:.4E}," + next(nl) for e, s in zip(eps, model.sig_p)]) + ")"
        nl_mat += """
Traction=DEFI_FONCTION(
    NOM_PARA='EPSI', NOM_RESU='SIGM', VALE=nl_mat, INTERPOL='LIN', PROL_DROITE='LINEAIRE', PROL_GAUCHE='CONSTANT'
)"""
        mat_nl_in = ", TRACTION=_F(SIGM=Traction,)"
    else:
        logging.debug(f"No plasticity is defined for material {material.name}")
        nl_mat = ""
        mat_nl_in = ""

    return f"""{nl_mat}

{material.name} = DEFI_MATERIAU(
    ELAS=_F(E={model.E}, NU={model.v}, RHO={model.rho}){mat_nl_in},
)
"""


def write_sections(fem_sections: FemSections) -> str:
    mat_assign_str = ""

    beam_sections_str = "\n        POUTRE=(),"
    shell_sections_str = "\n        COQUE=(),"
    solid_sections_str = ""

    if len(fem_sections.shells) > 0:
        mat_assign_str_, shell_sections_str = [
            "".join(x) for x in zip(*[write_shell_section(sh) for sh in fem_sections.shells])
        ]
        mat_assign_str += mat_assign_str_
        shell_sections_str = f"\n        COQUE=(\n{shell_sections_str}\n        ),"

    if len(fem_sections.lines) > 0:
        mat_assign_str_, beam_sections_str, orientations_str = [
            "".join(x) for x in zip(*[write_beam_section(bm) for bm in fem_sections.lines])
        ]
        mat_assign_str += mat_assign_str_
        beam_sections_str = f"\n        POUTRE=(\n{beam_sections_str}\n        ),"
        beam_sections_str += f"\n        ORIENTATION=(\n{orientations_str}\n        ),"

    if len(fem_sections.solids) > 0:
        mat_assign_str += write_solid_section(fem_sections.solids)

    return f"""
material = AFFE_MATERIAU(
    MODELE=model,
    AFFE=(
{mat_assign_str}
    )
)


# Shell elements:
#   EPAIS: thickness
#   VECTEUR: a direction of reference in the tangent plan

element = AFFE_CARA_ELEM(
        MODELE=model,{shell_sections_str}{beam_sections_str}{solid_sections_str}
    )
"""


def write_shell_section(fem_sec: FemSection) -> Tuple[str, str]:
    mat_name = fem_sec.material.name
    sec_name = fem_sec.elset.name
    #
    local_vec = str(tuple(fem_sec.local_y))
    mat_ = f'		_F(MATER=({mat_name},), GROUP_MA="{sec_name}"),\n'
    sec_str = f"""            _F(
                GROUP_MA=("{sec_name}"),
                EPAIS={fem_sec.thickness},
                VECTEUR={local_vec},
            ),
"""
    return mat_, sec_str


def write_beam_section(fem_sec: FemSection) -> Tuple[str, str, str]:
    mat_name = fem_sec.material.name
    sec_name = fem_sec.elset.name
    p = fem_sec.section.properties

    values = ",".join([str(x) for x in [p.Ax, p.Iy, p.Iz, p.Ix]])

    local_vec = str(tuple(fem_sec.local_y))

    mat_ = f'		_F(MATER=({mat_name},), GROUP_MA="{sec_name}"),\n'
    sec_str = f"""            _F(
                GROUP_MA=("{sec_name}"),
                SECTION = 'GENERALE',
                CARA = ('A', 'IY', 'IZ', 'JX'),
                VALE = ({values})
            ),
"""
    orientations = f"""            _F(
                GROUP_MA = '{sec_name}',
                CARA = 'VECT_Y',
                VALE = {local_vec}
            ),
"""

    return mat_, sec_str, orientations


def write_solid_section(fem_sections: Iterable[FemSection]) -> str:
    mat_ = ""
    for fsec in fem_sections:
        mat_ += f'		_F(MATER=({fsec.material.name},), GROUP_MA="{fsec.elset.name}"),\n'
    return mat_


def is_parent_of_node_solid(no: Node) -> bool:
    refs = no.refs
    for elem in refs:
        if elem.type in ElemShapeTypes.volume:
            return True
    return False


def create_bc_str(bc: Bc) -> str:
    set_name = bc.fem_set.name
    is_solid = False
    for no in bc.fem_set.members:
        is_solid = is_parent_of_node_solid(no)
        if is_solid:
            break
    dofs = ["DX", "DY", "DZ"]
    if is_solid is False:
        dofs += ["DRX", "DRY", "DRZ"]
    bc_str = ""
    for i, n in enumerate(dofs, start=1):
        if i in bc.dofs:
            bc_str += f"{n}=0, "
    dofs_str = f"""dofs = dict(
    GROUP_NO="{set_name}",
    {bc_str}
)\n"""

    return (
        dofs_str
        + f"""{bc.name} = AFFE_CHAR_MECA(
    MODELE=model, DDL_IMPO=_F(**dofs)
)"""
    )


def step_static_str(step: StepImplicit, part: Part) -> str:
    from ada.fem.exceptions.model_definition import (
        NoBoundaryConditionsApplied,
        NoLoadsApplied,
    )

    load_str = "\n".join(list(map(write_load, step.loads)))
    if len(step.loads) == 0:
        raise NoLoadsApplied(f"No loads are applied in step '{step}'")
    load = step.loads[0]
    all_boundary_conditions = part.get_assembly().fem.bcs + part.fem.bcs
    if len(all_boundary_conditions) == 0:
        raise NoBoundaryConditionsApplied("No boundary condition is found for the specified model")

    bc_str = ""
    for bc in all_boundary_conditions:
        bc_str += f"_F(CHARGE={bc.name}),"

    if step.nl_geom is False:
        return f"""
{load_str}

result = MECA_STATIQUE(
    MODELE=model,
    CHAM_MATER=material,
    EXCIT=({bc_str}_F(CHARGE={load.name}))
)

result = CALC_CHAMP(
    reuse=result,
    RESULTAT=result,
    CONTRAINTE=("SIGM_ELGA", "SIGM_ELNO"),
    CRITERES=("SIEQ_ELGA", "SIEQ_ELNO"),
)

IMPR_RESU(
    RESU=_F(RESULTAT=result),
    UNITE=80
)

"""
    else:
        return f"""
{load_str}

timeReel = DEFI_LIST_REEL(DEBUT=0.0, INTERVALLE=_F(JUSQU_A=1.0, NOMBRE=10))
timeInst = DEFI_LIST_INST(METHODE="AUTO", DEFI_LIST=_F(LIST_INST=timeReel))
rampFunc = DEFI_FONCTION(NOM_PARA="INST", VALE=(0.0, 0.0, 1.0, 1.0))

result = STAT_NON_LINE(
    MODELE=model,
    CHAM_MATER=material,
    CARA_ELEM=element,
    COMPORTEMENT=(_F(DEFORMATION="PETIT", RELATION="VMIS_ISOT_TRAC", TOUT="OUI")),
    CONVERGENCE=_F(ARRET="OUI", ITER_GLOB_MAXI=8,),
    EXCIT=({bc_str}_F(CHARGE={load.name}, FONC_MULT=rampFunc)),
    INCREMENT=_F(LIST_INST=timeInst),
    ARCHIVAGE=_F(LIST_INST=timeReel),
)

result = CALC_CHAMP(
    reuse=result, RESULTAT=result,
    CONTRAINTE=("EFGE_ELNO", "EFGE_NOEU", "SIGM_ELNO"),
    DEFORMATION=("EPSI_ELNO", "EPSP_ELNO"),
)

stress = POST_CHAMP(
    EXTR_COQUE=_F(
        NIVE_COUCHE='MOY',
    NOM_CHAM=('SIGM_ELNO', ),
    NUME_COUCHE=1),
    RESULTAT=result
)

stress = CALC_CHAMP(
    reuse=stress,
    CONTRAINTE=('SIGM_NOEU', ),
    RESULTAT=stress
)

strain = POST_CHAMP(
    EXTR_COQUE=_F(
        NIVE_COUCHE='MOY',
    NOM_CHAM=('EPSI_ELNO', ),
    NUME_COUCHE=1),
    RESULTAT=result
)

strainP = POST_CHAMP(
    EXTR_COQUE=_F(
        NIVE_COUCHE='MOY',
    NOM_CHAM=('EPSP_ELNO', ),
    NUME_COUCHE=1),
    RESULTAT=result
)

IMPR_RESU(
    RESU=(
        _F(
            NOM_CHAM=("DEPL", "EFGE_ELNO", "EFGE_NOEU"),
            NOM_CHAM_MED=("DISP", "GEN_FORCES_ELEM", "GEN_FORCES_NODES"),
            RESULTAT=result,
        ),
        _F(
            NOM_CHAM=("SIGM_ELNO", "SIGM_NOEU"),
            NOM_CHAM_MED=("STRESSES_ELEM", "STRESSES_NODES"),
            RESULTAT=stress,
        ),
        _F(
            NOM_CHAM=("EPSI_ELNO",),
            NOM_CHAM_MED=("STRAINS_ELEM",),
            RESULTAT=strain,
        ),
        _F(
            NOM_CHAM=("EPSP_ELNO",),
            NOM_CHAM_MED=("PLASTIC_STRAINS_ELEM",),
            RESULTAT=strainP,
        ),
    ),
    UNITE=80,
)"""


def step_eig_str(step: StepEigen, part: Part) -> str:
    bcs = part.fem.bcs + part.get_assembly().fem.bcs

    if len(bcs) > 1 or len(bcs) == 0:

        raise NotImplementedError("Number of BC sets is for now limited to 1 for eigenfrequency analysis")

    eig_map = dict(sorensen="SORENSEN", lanczos="TRI_DIAG")
    eig_type = step.metadata.get("eig_method", "sorensen")
    eig_method = eig_map[eig_type]

    # TODO: Add check for second order shell elements. If exists add conversion of results back from TRI7 to TRI6
    _ = """
    model_0 = AFFE_MODELE(
    AFFE=(
        _F(GROUP_MA=sh_2nd_order_sets, PHENOMENE='MECANIQUE', MODELISATION='MEMBRANE',),
    ),
    MAILLAGE=mesh
)

modes_0 = PROJ_CHAMP(
    MODELE_1=model,
    MODELE_2=model_0,
    RESULTAT=modes
)"""

    bc = bcs[0]
    return f"""
#modal analysis
ASSEMBLAGE(
    MODELE=model,
    CHAM_MATER=material,
    CARA_ELEM=element,
    CHARGE={bc.name},
    NUME_DDL=CO('dofs_eig'),
    MATR_ASSE = (
        _F(MATRICE=CO('stiff'), OPTION ='RIGI_MECA',),
        _F(MATRICE=CO('mass'), OPTION ='MASS_MECA', ),
    ),
)
# Using Subspace Iteration method ('SORENSEN' AND 'PLUS_PETITE')
# See https://www.code-aster.org/V2/UPLOAD/DOC/Formations/01-modal-analysis.pdf for more information
#

modes = CALC_MODES(
    CALC_FREQ=_F(NMAX_FREQ={step.num_eigen_modes}, ) ,
    SOLVEUR_MODAL=_F(METHODE='{eig_method}'),
    MATR_MASS=mass,
    MATR_RIGI=stiff,
    OPTION='PLUS_PETITE',
    VERI_MODE=_F(STOP_ERREUR='NON')
)



IMPR_RESU(
    RESU=_F(RESULTAT=modes, TOUT_CHAM='OUI'),
    UNITE=80
)
"""


def create_step_str(step: Union[StepEigen, StepImplicit], part: Part) -> str:
    st = StepEigen.TYPES
    step_map = {st.STATIC: step_static_str, st.EIGEN: step_eig_str}

    step_writer = step_map.get(step.type, None)

    if step_writer is None:
        raise NotImplementedError(f'Step type "{step.type}" is not yet supported')

    return step_writer(step, part)


def _write_nodes(part: Part, time_step, profile, families):
    """

    TODO: Go through each data group and set in HDF5 file and make sure that it writes what was read 1:1.
        Use cylinder.med as a benchmark.

    Add the following datasets ['COO', 'FAM', 'NUM'] to the 'NOE' group

    :param part:
    :param time_step:
    :param profile:
    :return:
    """
    points = np.zeros((int(part.fem.nodes.max_nid), 3))

    def pmap(n):
        points[int(n.id - 1)] = n.p

    list(map(pmap, part.fem.nodes))

    # Try this
    if _Settings.ca_experimental_id_numbering is True:
        points = np.array([n.p for n in part.fem.nodes])

    nodes_group = time_step.create_group("NOE")
    nodes_group.attrs.create("CGT", 1)
    nodes_group.attrs.create("CGS", 1)

    nodes_group.attrs.create("PFL", np.string_(profile))
    coo = nodes_group.create_dataset("COO", data=points.flatten(order="F"))
    coo.attrs.create("CGT", 1)
    coo.attrs.create("NBR", len(points))

    if _Settings.ca_experimental_id_numbering is True:
        node_ids = [n.id for n in part.fem.nodes]
        num = nodes_group.create_dataset("NUM", data=node_ids)
        num.attrs.create("CGT", 1)
        num.attrs.create("NBR", len(points))

    if len(part.fem.nsets.keys()) > 0:
        _add_node_sets(nodes_group, part, points, families)


def _write_elements(part: Part, time_step, profile, families):
    """

    Add the following ['FAM', 'NOD', 'NUM'] to the 'MAI' group

    **NOD** requires 'CGT' and 'NBR' attrs

    :param part:
    :param time_step:
    :param profile:
    :param families:
    :return:
    """

    def get_node_ids_from_element(el_):
        return [int(n.id) for n in el_.nodes]

    elements_group = time_step.create_group("MAI")
    elements_group.attrs.create("CGT", 1)
    for group, elements in part.fem.elements.group_by_type():
        if group in ElemShapeTypes.masses + ElemShapeTypes.springs:
            logging.error("NotImplemented: Skipping Mass or Spring Elements")
            continue
        med_type = abaqus_to_med_type(group)
        elements = list(elements)
        cells = np.array(list(map(get_node_ids_from_element, elements)))

        med_cells = elements_group.create_group(med_type)
        med_cells.attrs.create("CGT", 1)
        med_cells.attrs.create("CGS", 1)
        med_cells.attrs.create("PFL", np.string_(profile))

        nod = med_cells.create_dataset("NOD", data=cells.flatten(order="F"))
        nod.attrs.create("CGT", 1)
        nod.attrs.create("NBR", len(cells))

        # Node Numbering is necessary for proper handling of
        num = med_cells.create_dataset("NUM", data=[int(el.id) for el in elements])
        num.attrs.create("CGT", 1)
        num.attrs.create("NBR", len(cells))

    # Add Element sets
    if len(part.fem.elsets.keys()) > 0:
        _add_cell_sets(elements_group, part, families)


def _write_mesh_presets(f, mesh_name):
    """

    :param f:
    :param mesh_name:
    :return: Time step 0
    """
    numpy_void_str = np.string_("")
    dim = 3

    # Meshes
    mesh_ensemble = f.create_group("ENS_MAA")

    med_mesh = mesh_ensemble.create_group(mesh_name)
    med_mesh.attrs.create("DIM", dim)  # mesh dimension
    med_mesh.attrs.create("ESP", dim)  # spatial dimension
    med_mesh.attrs.create("REP", 0)  # cartesian coordinate system (repère in French)
    med_mesh.attrs.create("UNT", numpy_void_str)  # time unit
    med_mesh.attrs.create("UNI", numpy_void_str)  # spatial unit
    med_mesh.attrs.create("SRT", 1)  # sorting type MED_SORT_ITDT

    # component names:
    names = ["X", "Y", "Z"][:dim]
    med_mesh.attrs.create("NOM", np.string_("".join(f"{name:<16}" for name in names)))
    med_mesh.attrs.create("DES", np.string_("Mesh created with adapy"))
    med_mesh.attrs.create("TYP", 0)  # mesh type (MED_NON_STRUCTURE)

    # Time-step
    step = "-0000000000000000001-0000000000000000001"  # NDT NOR
    time_step = med_mesh.create_group(step)
    time_step.attrs.create("CGT", 1)
    time_step.attrs.create("NDT", -1)  # no time step (-1)
    time_step.attrs.create("NOR", -1)  # no iteration step (-1)
    time_step.attrs.create("PDT", -1.0)  # current time
    return time_step


def resolve_ids_in_multiple(tags, tags_data, is_elem):
    """Find elements shared by multiple sets"""
    from ada.fem import FemSet

    rmap = {tuple(v): r for r, v in tags.items()}
    fin_data = dict()
    for t, memb in tags_data.items():
        fin_data[t] = []
        for mem in memb:
            refs = list(filter(lambda x: type(x) == FemSet, mem.refs))
            if len(refs) > 1:
                names = [r.name for r in refs]
                if names not in tags.values():
                    new_int = min(tags.keys()) - 1 if is_elem else max(tags.keys()) + 1
                    tags[new_int] = names
                    rmap[tuple(names)] = new_int
                    fin_data[new_int] = []
                else:
                    new_int = rmap[tuple(names)]
                if mem not in fin_data[new_int]:
                    fin_data[new_int].append(mem)
            else:
                fin_data[t].append(mem)
    to_be_removed = []
    for i, f in fin_data.items():
        if len(f) == 0:
            to_be_removed.append(i)
    for t in to_be_removed:
        fin_data.pop(t)
        tags.pop(t)
    return fin_data


def _add_cell_sets(cells_group, part: Part, families):
    """

    :param cells_group:
    :param part:
    :param families:
    """
    cell_id_num = -4

    element = families.create_group("ELEME")
    tags = dict()
    tags_data = dict()

    cell_id_current = cell_id_num
    for cell_set in part.fem.elsets.values():
        tags[cell_id_current] = [cell_set.name]
        tags_data[cell_id_current] = cell_set.members
        cell_id_current -= 1

    res_data = resolve_ids_in_multiple(tags, tags_data, True)

    def get_node_ids_from_element(el_):
        return [int(n.id - 1) for n in el_.nodes]

    for group, elements in part.fem.elements.group_by_type():
        if group in ElemShapeTypes.masses + ElemShapeTypes.springs:
            logging.error("NotImplemented: Skipping Mass or Spring Elements")
            continue
        elements = list(elements)
        cell_ids = {el.id: i for i, el in enumerate(elements)}

        cell_data = np.zeros(len(elements), dtype=np.int32)

        for t, mem in res_data.items():
            list_filtered = [cell_ids[el.id] for el in filter(lambda x: x.type == group, mem)]
            for index in list_filtered:
                cell_data[index] = t

        cells = np.array(list(map(get_node_ids_from_element, elements)))
        med_type = abaqus_to_med_type(group)
        med_cells = cells_group.get(med_type)
        family = med_cells.create_dataset("FAM", data=cell_data)
        family.attrs.create("CGT", 1)
        family.attrs.create("NBR", len(cells))

    _write_families(element, tags)


def _add_node_sets(nodes_group, part: Part, points, families):
    """
    :param nodes_group:
    :param part:
    :param families:
    """
    tags = dict()
    nsets = dict()
    for key, val in part.fem.nsets.items():
        nsets[key] = [int(p.id) for p in val]

    points = _set_to_tags(nsets, points, 2, tags)

    family = nodes_group.create_dataset("FAM", data=points)
    family.attrs.create("CGT", 1)
    family.attrs.create("NBR", len(points))

    # For point tags
    node = families.create_group("NOEUD")
    _write_families(node, tags)


def _resolve_element_in_use_by_other_set(tagged_data, ind, tags, name, is_elem):
    existing_id = int(tagged_data[ind])
    current_tags = tags[existing_id]
    all_tags = current_tags + [name]

    if name in current_tags:
        logging.error("Unexpected error. Name already exists in set during resolving set members.")

    new_int = None
    for i_, t_ in tags.items():
        if all_tags == t_:
            new_int = i_
            break

    if new_int is None:
        new_int = int(min(tags.keys()) - 1) if is_elem else int(max(tags.keys()) + 1)
        tags[new_int] = tags[existing_id] + [name]

    tagged_data[ind] = new_int


def _set_to_tags(sets, data, tag_start_int, tags, id_map=None):
    """

    :param sets:
    :param data:
    :param tag_start_int:
    :param
    :return: The tagged data.
    """
    tagged_data = np.zeros(len(data), dtype=np.int32)
    tag_int = 0 + tag_start_int

    is_elem = False if tag_int > 0 else True

    tag_int = tag_start_int
    tag_map = dict()
    # Generate basic tags upfront
    for name in sets.keys():
        tags[tag_int] = [name]
        tag_map[name] = tag_int
        if is_elem is True:
            tag_int -= 1
        else:
            tag_int += 1

    for name, set_data in sets.items():
        if len(set_data) == 0:
            continue

        for index_ in set_data:
            index = int(index_ - 1)

            if id_map is not None:
                index = id_map[index_]

            if index > len(tagged_data) - 1:
                raise IndexError()

            if tagged_data[index] != 0:  # id is already defined in another set
                _resolve_element_in_use_by_other_set(tagged_data, index, tags, name, is_elem)
            else:
                tagged_data[index] = tag_map[name]

    return tagged_data


def _family_name(set_id, name):
    """Return the FAM object name corresponding to the unique set id and a list of subset names"""
    return "FAM" + "_" + str(set_id) + "_" + "_".join(name)


def _write_families(fm_group, tags):
    """Write point/cell tag information under FAS/[mesh_name]"""
    for set_id, name in tags.items():
        family = fm_group.create_group(_family_name(set_id, name))
        family.attrs.create("NUM", set_id)
        group = family.create_group("GRO")
        group.attrs.create("NBR", len(name))  # number of subsets
        dataset = group.create_dataset("NOM", (len(name),), dtype="80int8")
        for i in range(len(name)):
            # make name 80 characters
            name_80 = name[i] + "\x00" * (80 - len(name[i]))
            # Needs numpy array, see <https://github.com/h5py/h5py/issues/1735>
            dataset[i] = np.array([ord(x) for x in name_80])
