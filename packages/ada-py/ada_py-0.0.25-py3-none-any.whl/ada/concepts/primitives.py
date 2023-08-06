from __future__ import annotations

import logging
import pathlib
from dataclasses import dataclass
from typing import List, Tuple, Union

import numpy as np

from ada.base.physical_objects import BackendGeom
from ada.core.utils import Counter, roundoff, unit_vector, vector_length
from ada.ifc.utils import create_guid
from ada.materials import Material
from ada.materials.utils import get_material

from .curves import CurvePoly
from .points import Node
from .transforms import Placement


class Shape(BackendGeom):
    def __init__(
        self,
        name,
        geom,
        colour=None,
        opacity=1.0,
        mass: float = None,
        cog: Tuple[float, float, float] = None,
        metadata=None,
        units="m",
        ifc_elem=None,
        guid=None,
        material: Union[Material, str] = None,
        placement=Placement(),
    ):

        super().__init__(name, guid=guid, metadata=metadata, units=units, ifc_elem=ifc_elem, placement=placement)
        if type(geom) in (str, pathlib.WindowsPath, pathlib.PurePath, pathlib.Path):
            from OCC.Extend.DataExchange import read_step_file

            geom = read_step_file(str(geom))

        if ifc_elem is not None:
            self.guid = ifc_elem.GlobalId
            self._import_from_ifc_elem(ifc_elem)

        self._geom = geom
        self._mass = mass
        self._cog = cog
        self.colour = colour
        self._opacity = opacity
        if isinstance(material, Material):
            self._material = material
        else:
            self._material = get_material(material)

    def generate_ifc_solid_geom(self, f):
        raise NotImplementedError()

    def generate_parametric_solid(self, f):
        context = f.by_type("IfcGeometricRepresentationContext")[0]

        solid_geom = self.generate_ifc_solid_geom(f)

        if type(self) is Penetration:
            raise ValueError(f'Penetration type "{self}" is not yet supported')

        shape_representation = f.create_entity("IfcShapeRepresentation", context, "Body", "SweptSolid", [solid_geom])
        ifc_shape = f.create_entity("IfcProductDefinitionShape", None, None, [shape_representation])

        # Link to representation context
        for rep in ifc_shape.Representations:
            rep.ContextOfItems = context

        return ifc_shape

    def _generate_ifc_elem(self):
        from ada.ifc.utils import (
            add_colour,
            create_local_placement,
            create_property_set,
            get_tolerance,
            tesselate_shape,
        )

        if self.parent is None:
            raise ValueError("Parent cannot be None for IFC export")

        a = self.parent.get_assembly()
        f = a.ifc_file

        context = f.by_type("IfcGeometricRepresentationContext")[0]
        owner_history = a.user.to_ifc()
        parent = self.parent.get_ifc_elem()
        schema = a.ifc_file.wrapped_data.schema

        shape_placement = create_local_placement(f, relative_to=parent.ObjectPlacement)
        if type(self) is not Shape:
            ifc_shape = self.generate_parametric_solid(f)
        else:
            tol = get_tolerance(a.units)
            serialized_geom = tesselate_shape(self.geom, schema, tol)
            ifc_shape = f.add(serialized_geom)

        # Link to representation context
        for rep in ifc_shape.Representations:
            rep.ContextOfItems = context

        guid = self.metadata.get("guid", create_guid())
        description = self.metadata.get("description", None)

        if "hidden" in self.metadata.keys():
            if self.metadata["hidden"] is True:
                a.presentation_layers.append(ifc_shape)

        # Add colour
        if self.colour is not None:
            add_colour(f, ifc_shape.Representations[0].Items[0], str(self.colour), self.colour)

        ifc_elem = f.create_entity(
            "IfcBuildingElementProxy",
            guid,
            owner_history,
            self.name,
            description,
            None,
            shape_placement,
            ifc_shape,
            None,
            None,
        )

        for pen in self._penetrations:
            # elements.append(pen.ifc_opening)
            f.createIfcRelVoidsElement(
                create_guid(),
                owner_history,
                None,
                None,
                ifc_elem,
                pen.ifc_opening,
            )

        props = create_property_set("Properties", f, self.metadata)
        f.create_entity(
            "IfcRelDefinesByProperties",
            create_guid(),
            owner_history,
            "Properties",
            None,
            [ifc_elem],
            props,
        )

        return ifc_elem

    def _import_from_ifc_elem(self, ifc_elem):
        from ada.ifc.utils import getIfcPropertySets

        props = getIfcPropertySets(ifc_elem)
        if props is None:
            return None
        product_name = ifc_elem.Name
        if "NAME" in props.keys():
            name = props["NAME"] if product_name is None else product_name
        else:
            name = product_name if product_name is not None else "Test"

        if name is None or len(props.keys()) == 0:
            return None

        return Shape(
            name,
            None,
            guid=ifc_elem.GlobalId,
            metadata=dict(props=props, ifc_source=True),
        )

    @property
    def type(self):
        return type(self.geom)

    @property
    def transparent(self):
        return False if self.opacity == 1.0 else True

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        if 0.0 <= value <= 1.0:
            self._opacity = value
        else:
            raise ValueError("Opacity is only valid between 1 and 0")

    @property
    def mass(self) -> float:
        return self._mass

    @mass.setter
    def mass(self, value: float):
        self._mass = value

    @property
    def cog(self) -> Tuple[float, float, float]:

        return self._cog

    @cog.setter
    def cog(self, value: Tuple[float, float, float]):
        self._cog = value

    @property
    def bbox(self):
        """return the bounding box of the TopoDS_Shape `shape`

        returns xmin, ymin, zmin, xmax, ymax, zmax, xmax - xmin, ymax - ymin, zmax - zmin
        """
        from ada.occ.utils import get_boundingbox

        return get_boundingbox(self.geom, use_mesh=True)

    @property
    def point_on(self):
        return self.bbox[3:6]

    @property
    def geom(self):
        """

        :return:
        :rtype: OCC.Core.TopoDS.TopoDS_Shape
        """
        from ada.occ.utils import apply_penetrations

        if self._geom is None:
            from ada.ifc.utils import get_ifc_shape

            if self._ifc_elem is not None:
                ifc_elem = self._ifc_elem
            elif "ifc_file" in self.metadata.keys():
                a = self.parent.get_assembly()
                ifc_file = self.metadata["ifc_file"]
                ifc_f = a.get_ifc_source_by_name(ifc_file)
                ifc_elem = ifc_f.by_guid(self.guid)
            else:
                raise ValueError("No geometry information attached to this element")
            geom, color, alpha = get_ifc_shape(ifc_elem, self.ifc_settings)
            self._geom = geom
            self.colour = color
            self._opacity = alpha

        geom = apply_penetrations(self._geom, self.penetrations)

        return geom

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value != self._units:
            from ada.core.utils import unit_length_conversion

            scale_factor = unit_length_conversion(self._units, value)
            if self._geom is not None:
                from ada.occ.utils import transform_shape

                self._geom = transform_shape(self.geom, scale_factor)
            if self.metadata.get("ifc_source") is True:
                logging.info("do something")

            self._units = value

    @property
    def material(self) -> Material:
        return self._material

    @material.setter
    def material(self, value):
        self._material = value


class PrimSphere(Shape):
    def __init__(self, name, cog, radius, **kwargs):
        from ada.occ.utils import make_sphere

        self.radius = radius
        super(PrimSphere, self).__init__(name=name, geom=make_sphere(cog, radius), cog=cog, **kwargs)

    def generate_ifc_solid_geom(self, f):
        from ada.core.constants import X, Z
        from ada.ifc.utils import create_ifc_placement, to_real

        opening_axis_placement = create_ifc_placement(f, to_real(self.cog), Z, X)
        return f.createIfcSphere(opening_axis_placement, float(self.radius))

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value != self._units:
            from ada.core.utils import unit_length_conversion
            from ada.occ.utils import make_sphere

            scale_factor = unit_length_conversion(self._units, value)
            self.cog = tuple([x * scale_factor for x in self.cog])
            self.radius = self.radius * scale_factor
            self._geom = make_sphere(self.cog, self.radius)
            self._units = value

    def __repr__(self):
        return f"PrimSphere({self.name})"


class PrimBox(Shape):
    """Primitive Box. Length, width & height are local x, y and z respectively"""

    def __init__(self, name, p1, p2, colour=None, opacity=1.0, metadata=None, units="m"):
        from ada.occ.utils import make_box_by_points

        self.p1 = p1
        self.p2 = p2
        self._sides = BoxSides(self)
        super(PrimBox, self).__init__(
            name=name,
            geom=make_box_by_points(p1, p2),
            colour=colour,
            opacity=opacity,
            metadata=metadata,
            units=units,
        )

    def generate_ifc_solid_geom(self, f):
        from ada.core.constants import O, X, Z
        from ada.ifc.utils import (
            create_ifc_placement,
            create_ifcextrudedareasolid,
            create_ifcpolyline,
        )

        p1 = self.p1
        p2 = self.p2
        points = [
            p1,
            (p1[0], p2[1], p1[2]),
            (p2[0], p2[1], p1[2]),
            (p2[0], p1[1], p1[2]),
        ]
        depth = p2[2] - p1[2]
        polyline = create_ifcpolyline(f, points)
        profile = f.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
        opening_axis_placement = create_ifc_placement(f, O, Z, X)
        return create_ifcextrudedareasolid(f, profile, opening_axis_placement, (0.0, 0.0, 1.0), depth)

    @property
    def sides(self) -> BoxSides:
        return self._sides

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value != self._units:
            from ada.core.utils import unit_length_conversion
            from ada.occ.utils import make_box_by_points

            scale_factor = unit_length_conversion(self._units, value)
            self.p1 = tuple([x * scale_factor for x in self.p1])
            self.p2 = tuple([x * scale_factor for x in self.p2])
            self._geom = make_box_by_points(self.p1, self.p2)
            self._units = value

    def __repr__(self):
        return f"PrimBox({self.name})"


@dataclass
class BoxSides:
    parent: PrimBox

    def _return_fem_nodes(self, pmin, pmax, fem=None):
        if fem is None and self.parent is not None and self.parent.parent.fem.is_empty() is False:
            fem = self.parent.parent.fem

        if fem is None:
            raise ValueError("No FEM data found. Cannot return FEM nodes")

        return fem.nodes.get_by_volume(p=pmin, vol_box=pmax)

    def _return_data(self, pmin, pmax, fem, return_fem_nodes) -> Union[Tuple[tuple, tuple], List[Node]]:
        if return_fem_nodes is True:
            return self._return_fem_nodes(pmin, pmax, fem)

        return pmin, pmax

    def _return_surface(self):
        pass

    def _get_dim(self):
        box = self.parent
        p1 = np.array(box.p1)
        p2 = np.array(box.p2)
        l, w, h = p2 - p1
        return l, w, h, p1, p2

    def top(self, tol=1e-3, return_fem_nodes=False, fem=None):
        """Top is at positive local Z"""
        l, w, h, p1, p2 = self._get_dim()

        z = self.parent.placement.zdir

        pmin = p1 + l * z - tol
        pmax = p2 + tol

        return self._return_data(pmin, pmax, fem, return_fem_nodes)

    def bottom(self, tol=1e-3, return_fem_nodes=False, fem=None):
        """Bottom is at negative local z"""
        l, w, h, p1, p2 = self._get_dim()

        z = self.parent.placement.zdir

        pmin = p1 - tol
        pmax = p2 - l * z + tol

        return self._return_data(pmin, pmax, fem, return_fem_nodes)

    def front(self, tol=1e-3, return_fem_nodes=False, fem=None):
        """Front is at positive local y"""
        l, w, h, p1, p2 = self._get_dim()

        y = self.parent.placement.ydir

        pmin = p1 + l * y - tol
        pmax = p2 + tol

        return self._return_data(pmin, pmax, fem, return_fem_nodes)

    def back(self, tol=1e-3, return_fem_nodes=False, fem=None):
        """Back is at negative local y"""
        l, w, h, p1, p2 = self._get_dim()

        y = self.parent.placement.ydir

        pmin = p1 - tol
        pmax = p2 - l * y + tol

        return self._return_data(pmin, pmax, fem, return_fem_nodes)


class PrimCyl(Shape):
    def __init__(self, name, p1, p2, r, **kwargs):
        from ada.occ.utils import make_cylinder_from_points

        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        self.r = r
        super(PrimCyl, self).__init__(name, make_cylinder_from_points(p1, p2, r), **kwargs)

    def generate_ifc_solid_geom(self, f):
        from ada.core.constants import Z
        from ada.ifc.utils import (
            create_ifc_placement,
            create_ifcextrudedareasolid,
            to_real,
        )

        p1 = self.p1
        p2 = self.p2
        r = self.r

        vec = np.array(p2) - np.array(p1)
        uvec = unit_vector(vec)
        vecdir = to_real(uvec)

        cr_dir = np.array([0, 0, 1])

        if vector_length(abs(uvec) - abs(cr_dir)) == 0.0:
            cr_dir = np.array([1, 0, 0])

        perp_dir = np.cross(uvec, cr_dir)

        if vector_length(perp_dir) == 0.0:
            raise ValueError("Perpendicular dir cannot be zero")

        create_ifc_placement(f, to_real(p1), vecdir, to_real(perp_dir))

        opening_axis_placement = create_ifc_placement(f, to_real(p1), vecdir, to_real(perp_dir))

        depth = vector_length(vec)
        profile = f.createIfcCircleProfileDef("AREA", self.name, None, r)
        return create_ifcextrudedareasolid(f, profile, opening_axis_placement, Z, depth)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        from ada.occ.utils import make_cylinder_from_points

        if value != self._units:
            from ada.core.utils import unit_length_conversion

            scale_factor = unit_length_conversion(self._units, value)
            self.p1 = [x * scale_factor for x in self.p1]
            self.p2 = [x * scale_factor for x in self.p2]
            self.r = self.r * scale_factor
            self._geom = make_cylinder_from_points(self.p1, self.p2, self.r)

    def __repr__(self):
        return f"PrimCyl({self.name})"


class PrimExtrude(Shape):
    def __init__(self, name, points2d, h, normal, origin, xdir, tol=1e-3, **kwargs):
        self._name = name
        poly = CurvePoly(
            points2d=points2d,
            normal=normal,
            origin=origin,
            xdir=xdir,
            tol=tol,
            parent=self,
        )
        self._poly = poly
        self._extrude_depth = h

        super(PrimExtrude, self).__init__(name, self._poly.make_extruded_solid(self._extrude_depth), **kwargs)

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value != self._units:
            from ada.core.utils import unit_length_conversion

            scale_factor = unit_length_conversion(self._units, value)
            self.poly.placement.origin = [x * scale_factor for x in self.poly.placement.origin]
            self._extrude_depth = self._extrude_depth * scale_factor
            self._units = value

    @property
    def poly(self):
        """

        :return:
        :rtype: CurvePoly
        """
        return self._poly

    @property
    def extrude_depth(self):
        return self._extrude_depth

    def generate_ifc_solid_geom(self, f):
        from ada.core.constants import O, X, Z
        from ada.ifc.utils import (
            create_ifc_placement,
            create_ifcextrudedareasolid,
            create_ifcindexpolyline,
        )

        # https://standards.buildingsmart.org/IFC/RELEASE/IFC4_1/FINAL/HTML/link/annex-e.htm
        # polyline = self.create_ifcpolyline(self.file, [p[:3] for p in points])
        normal = self.poly.normal
        h = self.extrude_depth
        points = [tuple(x.astype(float).tolist()) for x in self.poly.seg_global_points]
        seg_index = self.poly.seg_index
        polyline = create_ifcindexpolyline(f, points, seg_index)
        profile = f.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
        opening_axis_placement = create_ifc_placement(f, O, Z, X)
        return create_ifcextrudedareasolid(f, profile, opening_axis_placement, [float(n) for n in normal], h)

    def __repr__(self):
        return f"PrimExtrude({self.name})"


class PrimRevolve(Shape):
    """Revolved Primitive"""

    def __init__(self, name, points2d, origin, xdir, normal, rev_angle, tol=1e-3, **kwargs):
        self._name = name
        poly = CurvePoly(
            points2d=points2d,
            normal=[roundoff(x) for x in normal],
            origin=origin,
            xdir=[roundoff(x) for x in xdir],
            tol=tol,
            parent=self,
        )
        self._poly = poly
        self._revolve_angle = rev_angle
        self._revolve_axis = [roundoff(x) for x in poly.ydir]
        self._revolve_origin = origin
        super(PrimRevolve, self).__init__(
            name,
            self._poly.make_revolve_solid(
                self._revolve_axis,
                self._revolve_angle,
                self._revolve_origin,
            ),
            **kwargs,
        )

    def generate_ifc_solid_geom(self, f):
        from ada.core.constants import O, X, Z
        from ada.ifc.utils import (
            create_ifc_placement,
            create_ifcindexpolyline,
            create_ifcrevolveareasolid,
        )

        # https://standards.buildingsmart.org/IFC/RELEASE/IFC4_1/FINAL/HTML/link/annex-e.htm
        # 8.8.3.28 IfcRevolvedAreaSolid

        revolve_axis = [float(n) for n in self.revolve_axis]
        revolve_origin = [float(x) for x in self.revolve_origin]
        revolve_angle = self.revolve_angle
        points = [tuple(x.astype(float).tolist()) for x in self.poly.seg_global_points]
        seg_index = self.poly.seg_index
        polyline = create_ifcindexpolyline(f, points, seg_index)
        profile = f.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
        opening_axis_placement = create_ifc_placement(f, O, Z, X)
        return create_ifcrevolveareasolid(
            f,
            profile,
            opening_axis_placement,
            revolve_origin,
            revolve_axis,
            revolve_angle,
        )

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value != self._units:
            raise NotImplementedError()

    @property
    def poly(self):
        return self._poly

    @property
    def revolve_origin(self):
        return self._revolve_origin

    @property
    def revolve_axis(self):
        return self._revolve_axis

    @property
    def revolve_angle(self):
        return self._revolve_angle

    def __repr__(self):
        return f"PrimRevolve({self.name})"


class PrimSweep(Shape):
    def __init__(
        self,
        name,
        sweep_curve,
        normal,
        xdir,
        profile_curve_outer,
        profile_curve_inner=None,
        origin=None,
        tol=1e-3,
        **kwargs,
    ):
        if type(sweep_curve) is list:
            sweep_curve = CurvePoly(points3d=sweep_curve, is_closed=False)

        if type(profile_curve_outer) is list:
            origin = sweep_curve.placement.origin if origin is None else origin
            profile_curve_outer = CurvePoly(profile_curve_outer, origin=origin, normal=normal, xdir=xdir)

        sweep_curve.parent = self
        profile_curve_outer.parent = self

        self._sweep_curve = sweep_curve
        self._profile_curve_outer = profile_curve_outer
        self._profile_curve_inner = profile_curve_inner

        super(PrimSweep, self).__init__(name, self._sweep_geom(), **kwargs)

    def _sweep_geom(self):
        from ada.occ.utils import sweep_geom

        return sweep_geom(self.sweep_curve.wire, self.profile_curve_outer.wire)

    def generate_ifc_solid_geom(self, f):
        from ada.core.constants import O, X, Z
        from ada.ifc.utils import (
            create_ifc_placement,
            create_IfcFixedReferenceSweptAreaSolid,
        )

        sweep_curve = self.sweep_curve.get_ifc_elem()
        profile = f.create_entity("IfcArbitraryClosedProfileDef", "AREA", None, self.profile_curve_outer.get_ifc_elem())
        ifc_xdir = f.create_entity("IfcDirection", [float(x) for x in self.profile_curve_outer.xdir])
        opening_axis_placement = create_ifc_placement(f, O, Z, X)

        return create_IfcFixedReferenceSweptAreaSolid(
            f, sweep_curve, profile, opening_axis_placement, None, None, ifc_xdir
        )

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value != self._units:
            raise NotImplementedError()

    @property
    def sweep_curve(self):
        return self._sweep_curve

    @property
    def profile_curve_outer(self):
        return self._profile_curve_outer

    @property
    def profile_curve_inner(self):
        return self._profile_curve_inner

    def __repr__(self):
        return f"PrimSweep({self.name})"


class Penetration(BackendGeom):
    _name_gen = Counter(1, "Pen")
    """A penetration object. Wraps around a primitive"""
    # TODO: Maybe this should be evaluated for removal?
    def __init__(self, primitive, metadata=None, parent=None, units="m", guid=None):
        if issubclass(type(primitive), Shape) is False:
            raise ValueError(f'Unsupported primitive type "{type(primitive)}"')

        super(Penetration, self).__init__(primitive.name, guid=guid, metadata=metadata, units=units)
        self._primitive = primitive
        self._parent = parent
        self._ifc_opening = None

    def _generate_ifc_opening(self):
        from ada.core.constants import O, X, Z
        from ada.ifc.utils import add_multiple_props_to_elem, create_local_placement

        if self.parent is None:
            raise ValueError("This penetration has no parent")

        a = self.parent.parent.get_assembly()
        f = a.ifc_file

        geom_parent = self.parent.parent.get_ifc_elem()
        owner_history = a.user.to_ifc()

        # Create and associate an opening for the window in the wall
        opening_placement = create_local_placement(f, O, Z, X, geom_parent.ObjectPlacement)
        opening_shape = self.primitive.generate_parametric_solid(f)

        opening_element = f.createIfcOpeningElement(
            create_guid(),
            owner_history,
            self.name,
            self.name + " (Opening)",
            None,
            opening_placement,
            opening_shape,
            None,
        )

        add_multiple_props_to_elem(self.metadata.get("props", dict()), opening_element, f)

        return opening_element

    @property
    def primitive(self):
        return self._primitive

    @property
    def geom(self):
        return self.primitive.geom

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if value != self._units:
            self.primitive.units = value
            self._units = value

    @property
    def ifc_opening(self):
        if self._ifc_opening is None:
            self._ifc_opening = self._generate_ifc_opening()
        return self._ifc_opening

    def __repr__(self):
        return f"Pen(type={self.primitive})"
