"""Tests related to Edb modeler
"""

import pytest
from pyedb.generic.settings import settings

pytestmark = pytest.mark.system

class TestClass:
    @pytest.fixture(autouse=True)
    def init(self, edbapp, local_scratch, target_path, target_path2, target_path4):
        self.edbapp = edbapp
        self.local_scratch = local_scratch
        self.target_path = target_path
        self.target_path2 = target_path2
        self.target_path4 = target_path4

    def test_modeler_polygons(self):
        """Evaluate modeler polygons"""
        assert len(self.edbapp.modeler.polygons) > 0
        assert self.edbapp.modeler.polygons[0].is_void == self.edbapp.modeler.polygons[0].IsVoid()

        poly0 = self.edbapp.modeler.polygons[0]
        assert self.edbapp.modeler.polygons[0].clone()
        assert isinstance(poly0.voids, list)
        assert isinstance(poly0.points_raw(), list)
        assert isinstance(poly0.points(), tuple)
        assert isinstance(poly0.points()[0], list)
        assert poly0.points()[0][0] >= 0.0
        assert poly0.points_raw()[0].X.ToDouble() >= 0.0
        assert poly0.type == "Polygon"
        assert not poly0.is_arc(poly0.points_raw()[0])
        assert isinstance(poly0.voids, list)
        assert isinstance(poly0.get_closest_point([0, 0]), list)
        assert isinstance(poly0.get_closest_arc_midpoint([0, 0]), list)
        assert isinstance(poly0.arcs, list)
        assert isinstance(poly0.longest_arc.length, float)
        assert isinstance(poly0.shortest_arc.length, float)
        assert not poly0.in_polygon([0, 0])
        assert isinstance(poly0.arcs[0].center, list)
        assert isinstance(poly0.arcs[0].radius, float)
        assert poly0.arcs[0].is_segment
        assert not poly0.arcs[0].is_point
        assert not poly0.arcs[0].is_ccw
        assert isinstance(poly0.arcs[0].points_raw, list)
        assert isinstance(poly0.arcs[0].points, tuple)
        assert isinstance(poly0.intersection_type(poly0), int)
        assert poly0.is_intersecting(poly0)

    def test_modeler_paths(self):
        """Evaluate modeler paths"""
        assert len(self.edbapp.modeler.paths) > 0
        assert self.edbapp.modeler.paths[0].type == "Path"
        assert self.edbapp.modeler.paths[0].clone()
        assert isinstance(self.edbapp.modeler.paths[0].width, float)
        self.edbapp.modeler.paths[0].width = "1mm"
        assert self.edbapp.modeler.paths[0].width == 0.001

    def test_modeler_primitives_by_layer(self):
        """Evaluate modeler primitives by layer"""
        assert self.edbapp.modeler.primitives_by_layer["1_Top"][0].layer_name == "1_Top"
        assert self.edbapp.modeler.primitives_by_layer["1_Top"][0].layer.GetName() == "1_Top"
        assert not self.edbapp.modeler.primitives_by_layer["1_Top"][0].is_negative
        assert not self.edbapp.modeler.primitives_by_layer["1_Top"][0].is_void
        self.edbapp.modeler.primitives_by_layer["1_Top"][0].is_negative = True
        assert self.edbapp.modeler.primitives_by_layer["1_Top"][0].is_negative
        self.edbapp.modeler.primitives_by_layer["1_Top"][0].is_negative = False
        assert not self.edbapp.modeler.primitives_by_layer["1_Top"][0].has_voids
        assert not self.edbapp.modeler.primitives_by_layer["1_Top"][0].is_parameterized
        assert isinstance(self.edbapp.modeler.primitives_by_layer["1_Top"][0].get_hfss_prop(), tuple)
        assert not self.edbapp.modeler.primitives_by_layer["1_Top"][0].is_zone_primitive
        assert self.edbapp.modeler.primitives_by_layer["1_Top"][0].can_be_zone_primitive

    def test_modeler_primitives(self):
        """Evaluate modeler primitives"""
        assert len(self.edbapp.modeler.rectangles) > 0
        assert len(self.edbapp.modeler.circles) > 0
        assert len(self.edbapp.modeler.bondwires) == 0
        assert "1_Top" in self.edbapp.modeler.polygons_by_layer.keys()
        assert len(self.edbapp.modeler.polygons_by_layer["1_Top"]) > 0
        assert len(self.edbapp.modeler.polygons_by_layer["DE1"]) == 0
        assert self.edbapp.modeler.rectangles[0].type == "Rectangle"
        assert self.edbapp.modeler.circles[0].type == "Circle"

    def test_modeler_get_polygons_bounding(self):
        """Retrieve polygons bounding box."""
        polys = self.edbapp.modeler.get_polygons_by_layer("GND")
        for poly in polys:
            bounding = self.edbapp.modeler.get_polygon_bounding_box(poly)
            assert len(bounding) == 4

    def test_modeler_get_polygons_by_layer_and_nets(self):
        """Retrieve polygons by layer and nets."""
        nets = ["GND", "1V0"]
        polys = self.edbapp.modeler.get_polygons_by_layer("16_Bottom", nets)
        assert polys


    def test_modeler_get_polygons_points(self):
        """Retrieve polygons points."""
        polys = self.edbapp.modeler.get_polygons_by_layer("GND")
        for poly in polys:
            points = self.edbapp.modeler.get_polygon_points(poly)
            assert points

    def test_modeler_create_polygon(self):
        """Create a polygon based on a shape or points."""
        settings.enable_error_handler = True
        points = [
            [-0.025, -0.02],
            [0.025, -0.02],
            [0.025, 0.02],
            [-0.025, 0.02],
            [-0.025, -0.02],
        ]
        plane = self.edbapp.modeler.Shape("polygon", points=points)
        points = [
            [-0.001, -0.001],
            [0.001, -0.001, "ccw", 0.0, -0.0012],
            [0.001, 0.001],
            [0.0015, 0.0015, 0.0001],
            [-0.001, 0.0015],
            [-0.001, -0.001],
        ]
        void1 = self.edbapp.modeler.Shape("polygon", points=points)
        void2 = self.edbapp.modeler.Shape("rectangle", [-0.002, 0.0], [-0.015, 0.0005])
        assert self.edbapp.modeler.create_polygon(plane, "1_Top", [void1, void2])
        self.edbapp["polygon_pts_x"] = -1.025
        self.edbapp["polygon_pts_y"] = -1.02
        points = [
            ["polygon_pts_x", "polygon_pts_y"],
            [1.025, -1.02],
            [1.025, 1.02],
            [-1.025, 1.02],
            [-1.025, -1.02],
        ]
        assert self.edbapp.modeler.create_polygon(points, "1_Top")
        settings.enable_error_handler = False

    def test_modeler_create_trace(self):
        """Create a trace based on a list of points."""
        points = [
            [-0.025, -0.02],
            [0.025, -0.02],
            [0.025, 0.02],
        ]
        trace = self.edbapp.modeler.create_trace(points, "1_Top")
        assert trace
        assert isinstance(trace.get_center_line(), list)
        assert isinstance(trace.get_center_line(True), list)
        self.edbapp["delta_x"] = "1mm"
        assert trace.add_point("delta_x", "1mm", True)
        assert trace.get_center_line(True)[-1][0] == "(delta_x)+(0.025)"
        assert trace.add_point(0.001, 0.002)
        assert trace.get_center_line()[-1] == [0.001, 0.002]

    def test_modeler_add_void(self):
        """Add a void into a shape."""
        plane_shape = self.edbapp.modeler.Shape("rectangle", pointA=["-5mm", "-5mm"], pointB=["5mm", "5mm"])
        plane = self.edbapp.modeler.create_polygon(plane_shape, "1_Top", net_name="GND")
        void = self.edbapp.modeler.create_trace([["0", "0"], ["0", "1mm"]], layer_name="1_Top", width="0.1mm")
        assert self.edbapp.modeler.add_void(plane, void)
        assert plane.add_void(void)

    def test_modeler_fix_circle_void(self):
        """Fix issues when circle void are clipped due to a bug in EDB."""
        assert self.edbapp.modeler.fix_circle_void_for_clipping()

    def test_modeler_primitives_area(self):
        """Access primitives total area."""
        i = 0
        while i < 10:
            assert self.edbapp.modeler.primitives[i].area(False) > 0
            assert self.edbapp.modeler.primitives[i].area(True) > 0
            i += 1
        assert self.edbapp.modeler.primitives[i].bbox
        assert self.edbapp.modeler.primitives[i].center
        assert self.edbapp.modeler.primitives[i].get_closest_point((0, 0))
        assert self.edbapp.modeler.primitives[i].polygon_data
        assert self.edbapp.modeler.paths[0].length

    def test_modeler_create_rectangle(self):
        """Create rectangle."""
        rect = self.edbapp.modeler.create_rectangle("1_Top", "SIG1", ["0", "0"], ["2mm", "3mm"])
        assert rect
        rect.is_negative = True
        assert rect.is_negative
        rect.is_negative = False
        assert not rect.is_negative
        assert self.edbapp.modeler.create_rectangle(
            "1_Top",
            "SIG2",
            center_point=["0", "0"],
            width="4mm",
            height="5mm",
            representation_type="CenterWidthHeight",
        )

    def test_modeler_create_circle(self):
        """Create circle."""
        poly = self.edbapp.modeler.create_polygon_from_points([[0, 0], [100, 0], [100, 100], [0, 100]], "1_Top")
        assert poly
        poly.add_void([[20, 20], [20, 30], [100, 30], [100, 20]])
        poly2 = self.edbapp.modeler.create_polygon_from_points([[60, 60], [60, 150], [150, 150], [150, 60]], "1_Top")
        new_polys = poly.subtract(poly2)
        assert len(new_polys) == 1
        circle = self.edbapp.modeler.create_circle("1_Top", 40, 40, 15)
        assert circle
        intersection = new_polys[0].intersect(circle)
        assert len(intersection) == 1
        circle2 = self.edbapp.modeler.create_circle("1_Top", 20, 20, 15)
        assert circle2.unite(intersection)
