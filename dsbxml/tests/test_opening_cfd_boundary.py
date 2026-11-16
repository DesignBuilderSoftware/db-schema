from pathlib import Path

import dsbxml
from dsbxml.core import Opening

SAMPLE = (
    Path(__file__).resolve().parents[2] / "samples" / "2025.1.0.095" / "HVAC_Zones_Coloured.xml"
)

OPENING = """<Opening type="Hole">
  <Polygon auxiliaryType="2"><Vertices><Point3D>0; 0; 0</Point3D></Vertices>
  <PolygonHoles></PolygonHoles>
  </Polygon>
  <SegmentList>
    <CFDBoundary type="CFD natural ventilation outlet boundary">
      <Polygon auxiliaryType="0"><Vertices><Point3D>1; 2; 3</Point3D></Vertices>
      <PolygonHoles></PolygonHoles>
      </Polygon>
      <CFDBoundarySettings>
        <Temperature>20.0000</Temperature><FlowRate>0.5000</FlowRate>
        <XDirectionDischargeAngle>0</XDirectionDischargeAngle><YDirectionDischargeAngle>0</YDirectionDischargeAngle>
        <MultiWayDiffuserDischargeAngle>0</MultiWayDiffuserDischargeAngle>
        <TwoWayDiffuserDischargeDirection>0</TwoWayDiffuserDischargeDirection>
        <MinimumDischargeVelocity>1</MinimumDischargeVelocity><ActualDischargeVelocity>1</ActualDischargeVelocity>
        <HeatFlux>0</HeatFlux><Pressure>0</Pressure><PressureType>0</PressureType>
        <MoistureSource>0</MoistureSource><ContaminantSource>0</ContaminantSource><RelativeHumidity>0</RelativeHumidity>
        <NonOrthoElementWidth>0.5</NonOrthoElementWidth><NonOrthoElementHeight>0.5</NonOrthoElementHeight>
        <NonOrthoFaceOffset>0.4</NonOrthoFaceOffset><NonOrthoElementXSpacing>0.3</NonOrthoElementXSpacing>
        <NonOrthoElementYSpacing>0.3</NonOrthoElementYSpacing><NonOrthoElementXEdgeOffset>0.1</NonOrthoElementXEdgeOffset>
        <NonOrthoElementYEdgeOffset>0.1</NonOrthoElementYEdgeOffset><DiffuserElementDimension>0.2</DiffuserElementDimension>
        <RefinementRegionDistance>52.8751</RefinementRegionDistance><RefinementRegionLevel>2</RefinementRegionLevel>
      </CFDBoundarySettings>
      <MinimumRefinementRegionPoint><Point3D>0; 0; 0</Point3D></MinimumRefinementRegionPoint>
      <MaximumRefinementRegionPoint><Point3D>9; 9; 9</Point3D></MaximumRefinementRegionPoint>
      <CFDBoundaryComponentList></CFDBoundaryComponentList>
      <Attributes><Attribute key="CFDBoundaryRefinementRegionLevel">2</Attribute></Attributes>
    </CFDBoundary>
  </SegmentList>
</Opening>"""


def test_an_openings_segment_list_holds_its_cfd_boundary():
    boundary = Opening.from_xml(OPENING).segment_list.cfd_boundary
    assert boundary.type == "CFD natural ventilation outlet boundary"
    assert boundary.cfd_boundary_settings.temperature == 20.0
    assert boundary.cfd_boundary_settings.flowRate == 0.5
    assert boundary.cfd_boundary_settings.refinement_region_level == 2
    assert boundary.maximum_refinement_region_point.point_3d.value == "9; 9; 9"
    assert boundary.attributes.attribute[0].key == "CFDBoundaryRefinementRegionLevel"


def test_an_opening_with_lines_or_nothing_still_reads():
    plain = OPENING.split("<SegmentList>")[0] + "<SegmentList></SegmentList></Opening>"
    assert Opening.from_xml(plain).segment_list.cfd_boundary is None


def test_the_sample_reads_all_twelve_boundaries():
    model = dsbxml.dsbXML.from_xml(SAMPLE.read_bytes())
    found = [
        o.segment_list.cfd_boundary
        for b in model.site.buildings.building
        for bb in b.building_blocks.building_block
        for z in bb.zones.zone
        for s in z.body.surfaces.surface
        for o in (s.openings.opening if s.openings else [])
        if o.segment_list and o.segment_list.cfd_boundary
    ]
    assert len(found) == 12
    assert all(f.cfd_boundary_settings.minimumDischargeVelocity == 1.0 for f in found)
