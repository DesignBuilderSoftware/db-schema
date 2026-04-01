"""
core.py
====================================
The core module of the designbuilder_schema
"""


from typing import Optional, List, Annotated
from pydantic import field_serializer, Field, ConfigDict
from pydantic_xml import attr, element
from designbuilder_schema.hvac.network import HVACNetwork
from designbuilder_schema.base import BaseModel
from designbuilder_schema.id import ObjectIDs, current_site_handle
from designbuilder_schema.geometry import Point3D, Vertices, Line
from designbuilder_schema.tables import Tables
from designbuilder_schema.attributes import NameAttributes, KeyAttributes
import datetime


class dsbXML(BaseModel):
    """Root element of DesignBuilder XML file.

    Represents the top-level dsbXML element containing metadata and simulation data
    for a DesignBuilder project.

    Attributes:
        name: Name of the DesignBuilder project
        date: Creation/modification date of the file
        version: Version of the DesignBuilder format
        objects: Number of objects in the model
        site: The site definition containing buildings and geometry
    """
    model_config = ConfigDict(populate_by_name=True)

    name: str = attr()
    date: datetime.date = attr()
    version: str = attr()
    objects: str = attr()
    site: Optional["Site"] = element(default=None)

    @classmethod
    def from_xml(cls, source, **kwargs):
        """Override to handle PascalCase XML tags to snake_case Python fields"""
        from lxml import etree
        if isinstance(source, (str, bytes)):
            root = etree.fromstring(source)
        else:
            root = source

        # Rename PascalCase child elements to lowercase (iterative, non-recursive)
        # This handles XML like <Site> being mapped to field 'site'
        stack = [root]
        while stack:
            element = stack.pop()
            # Convert tag names: Site -> site, Tables -> tables, etc.
            if element.tag and len(element.tag) > 1 and element.tag[0].isupper():
                element.tag = element.tag[0].lower() + element.tag[1:]
            # Add children to stack for processing
            stack.extend(reversed(element))

        instance = super().from_xml_tree(root)
        return instance

    def to_xml(self, **kwargs) -> str | bytes:
        """Override to output dsbXML as root element"""
        from lxml import etree
        xml_output = super().to_xml(**kwargs)
        if isinstance(xml_output, bytes):
            root = etree.fromstring(xml_output)
            root.tag = "dsbXML"
            return etree.tostring(root, xml_declaration=True, encoding="UTF-8")
        else:
            root = etree.fromstring(xml_output.encode())
            root.tag = "dsbXML"
            return etree.tostring(root, xml_declaration=True, encoding="UTF-8").decode("UTF-8")


class Site(BaseModel):
    """Top-level site definition containing buildings and assemblies.

    Represents a site in DesignBuilder containing all buildings, construction
    assemblies, and simulation data tables.

    Attributes:
        count: Number of elements in the site
        handle: Unique identifier for the site
        attributes: Named attributes for the site
        tables: Simulation tables containing climate, schedules, and other data
        assembly_library: Library of assemblies used in the project
        buildings: Collection of buildings in the site
    """
    count: int = attr()
    handle: int = attr()
    attributes: "NameAttributes" = element(default_factory=lambda: NameAttributes())
    tables: Optional["Tables"] = element(default=None)
    assembly_library: Optional["AssemblyLibrary"] = element(default=None)
    buildings: Optional["Buildings"] = element(default=None)

    @field_serializer("handle")
    def serialize_handle(self, _) -> int:
        return current_site_handle()


class AssemblyLibrary(BaseModel):
    """Library of assemblies used in the model.

    Contains reusable assemblies that can be applied to multiple surfaces.

    Attributes:
        assemblyHandle: Unique identifier for the assembly library
        assembly: List of assembly definitions
    """
    assemblyHandle: int = attr()
    assembly: List["Assembly"] = element(tag="Assembly")


class Assembly(BaseModel):
    """A single assembly definition.

    Attributes:
        assemblyHandle: Unique identifier for this assembly
        componentBlockHandle: Reference to the component block containing layers
        reference: Reference identifier or name
        handle_point: Origin point for the assembly placement
        component_blocks: Collection of component blocks defining construction layers
        attributes: Key attributes for the assembly
    """
    assemblyHandle: int = attr()
    componentBlockHandle: int = attr()
    reference: str = attr()
    handle_point: "Point3D" = element()
    component_blocks: "ComponentBlocks" = element()
    attributes: "KeyAttributes" = element()


class ComponentBlocks(BaseModel):
    """Container for component block list.

    Attributes:
        component_block: List of component blocks
    """
    component_block: List["ComponentBlock"] = element(tag="ComponentBlock")


class ComponentBlock(BaseModel):
    """A single component block representing a construction layer or element.

    Attributes:
        type: Type identifier for the component block
        body: The 3D geometry body of this component
    """
    type: str = attr()
    body: "Body" = element()


class Body(BaseModel):
    """3D body geometry with surfaces and structural information.

    Represents a 3D volume with vertices, surfaces, and optional void bodies
    (e.g., window openings, atria).

    Attributes:
        volume: Volume of the body in cubic meters
        extrusionHeight: Height of extrusion used to create this body
        object_ids: Unique object identifiers
        vertices: List of 3D vertices defining the geometry
        surfaces: Collection of surfaces forming the body envelope
        void_perimeter_list: Perimeter polygons of void bodies (openings)
        attributes: Key attributes for the body
    """
    volume: float = attr()
    extrusionHeight: float = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    vertices: "Vertices" = element()
    surfaces: "Surfaces" = element()
    void_perimeter_list: Optional["VoidPerimeterList"] = element()
    attributes: Optional["KeyAttributes"] = element()


class Surfaces(BaseModel):
    """Container for surface list.

    Attributes:
        surface: List of surfaces
    """
    surface: List["Surface"] = element(tag="Surface")


class Surface(BaseModel):
    """A single surface (wall, floor, roof, etc.) with thermal and optical properties.

    Represents an individual building surface with geometry, material properties,
    and optional openings or thermal adjacencies.

    Attributes:
        type: Surface type identifier (wall, roof, floor, etc.)
        area: Surface area in square meters
        alpha: Solar absorptance/absorbance coefficient
        phi: Emissivity coefficient
        defaultOpenings: Default opening type for this surface
        adjacentPartitionHandle: Reference to adjacent partition
        thickness: Total thickness of construction
        object_ids: Unique object identifiers
        vertex_indices: Indices of vertices forming this surface
        hole_indices: Indices of holes (openings) in the surface
        openings: Collection of windows and doors
        adjacencies: Thermal adjacencies to other surfaces
        attributes: Key attributes for the surface
    """
    type: str = attr()
    area: float = attr()
    alpha: float = attr()
    phi: float = attr()
    defaultOpenings: str = attr()
    adjacentPartitionHandle: int = attr()
    thickness: float = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    vertex_indices: str = element()
    hole_indices: Optional[str] = element(default=None)
    openings: Optional["Openings"] = element()
    adjacencies: Optional["Adjacencies"] = element()
    attributes: Optional["KeyAttributes"] = element()


class Openings(BaseModel):
    """Container for opening (window/door) list.

    Attributes:
        opening: List of openings
    """
    opening: List["Opening"] = element(tag="Opening")


class Opening(BaseModel):
    """A single window or door opening in a surface.

    Represents an opening with geometry and optional CFD segments.

    Attributes:
        type: Opening type (window, door, etc.)
        polygon: Polygonal outline of the opening
        attributes: Key attributes for the opening
        segment_list: CFD mesh segments for this opening
    """
    type: str = attr()
    polygon: "Polygon" = element()
    attributes: Optional["KeyAttributes"] = element()
    segment_list: Optional["CFDSegmentList"] = element()


class Adjacencies(BaseModel):
    """Container for adjacency list.

    Attributes:
        adjacency: List of adjacencies
    """
    adjacency: List["Adjacency"] = element(tag="Adjacency")


class Adjacency(BaseModel):
    """Thermal adjacency between two surfaces in different zones.

    Defines how two surfaces exchange heat (e.g., party walls between adjacent spaces).

    Attributes:
        type: Adjacency type identifier
        adjacencyDistance: Distance between adjacent surfaces
        object_ids: Unique object identifiers
        adjacency_polygon_list: Overlapping polygon areas between surfaces
    """
    type: str = attr()
    adjacencyDistance: float = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    adjacency_polygon_list: "AdjacencyPolygonList" = element()


class AdjacencyPolygonList(BaseModel):
    """Container for adjacency polygon list.

    Attributes:
        polygon: List of overlapping polygons defining adjacency areas
    """
    polygon: List["Polygon"] = element(tag="Polygon")


class Buildings(BaseModel):
    """Container for building list.

    Attributes:
        numberOfBuildings: Count of buildings in the site
        building: List of building definitions
    """
    numberOfBuildings: int = attr()
    building: List["Building"] = element(tag="Building")


class Building(BaseModel):
    """A single building containing zones, surfaces, and HVAC systems.

    Represents a complete building with all its geometric and thermal components.

    Attributes:
        currentComponentBlockHandle: Handle to current component block
        currentAssemblyInstanceHandle: Handle to current assembly instance
        currentPlaneHandle: Handle to current plane
        object_ids: Unique object identifiers
        building_blocks: Structural building blocks (repeating elements)
        component_blocks: Individual component blocks
        assembly_instances: Instances of assemblies placed in the building
        profile_outlines: Building profile outlines for form visualization
        construction_lines: Construction/reference lines
        planes: Work planes used in the building definition
        hvac_network: HVAC heating/cooling system network
        bookmark_buildings: Navigation bookmarks for the building
        attributes: Key attributes for the building
    """
    currentComponentBlockHandle: int = attr()
    currentAssemblyInstanceHandle: int = attr()
    currentPlaneHandle: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    building_blocks: Optional["BuildingBlocks"] = element()
    component_blocks: Optional["ComponentBlocks"] = element()
    assembly_instances: Optional["AssemblyInstances"] = element()
    profile_outlines: Optional["ProfileOutlines"] = element()
    construction_lines: Optional["ConstructionLines"] = element()
    planes: Optional["Planes"] = element()
    hvac_network: Optional["HVACNetwork"] = element()
    bookmark_buildings: Optional["BookmarkBuildings"] = element()
    attributes: "KeyAttributes" = element()


class BuildingBlocks(BaseModel):
    """Container for building block list.

    Attributes:
        building_block: List of building blocks
    """
    building_block: List["BuildingBlock"] = element(tag="BuildingBlock")


class BuildingBlock(BaseModel):
    """A repeating structural block within a building.

    Represents a modular building component with defined dimensions and structural properties.

    Attributes:
        type: Block type identifier
        height: Height of the block
        roofSlope: Angle of roof slope
        roofOverlap: Roof overlap dimension
        roofType: Type of roof (flat, pitched, etc.)
        wallSlope: Angle of wall slope
        object_ids: Unique object identifiers
        component_blocks: Structural component layers
        cfd_fans: CFD fans and ventilation components
        assembly_instances: Assembly instances within this block
        profile_outlines: Profile outlines for visualization
        internal_partitions: Internal walls and dividers
        void_bodies: Atria and internal voids
        zones: Thermal zones within this block
        profile_body: Overall profile body geometry
        perimeter: Perimeter definition
        base_profile_body: Base profile for extrusion
        attributes: Key attributes for the block
    """
    type: str = attr()
    height: float = attr()
    roofSlope: float = attr()
    roofOverlap: float = attr()
    roofType: str = attr()
    wallSlope: float = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    component_blocks: Optional["ComponentBlocks"] = element()
    cfd_fans: Optional["CFDFans"] = element()
    assembly_instances: Optional["AssemblyInstances"] = element()
    profile_outlines: Optional["ProfileOutlines"] = element()
    internal_partitions: Optional["InternalPartitions"] = element()
    void_bodies: Optional["VoidBodies"] = element()
    zones: Optional["Zones"] = element()
    profile_body: Optional["ProfileBody"] = element()
    perimeter: Optional["Perimeter"] = element()
    base_profile_body: Optional["BaseProfileBody"] = element()
    attributes: "KeyAttributes" = element()


class InternalPartitions(BaseModel):
    """Container for internal partition list.

    Attributes:
        internal_partition: List of internal partitions
    """
    internal_partition: List["InternalPartition"] = element(tag="InternalPartition")


class InternalPartition(BaseModel):
    """An internal wall or partition dividing zones.

    Represents non-structural internal surfaces such as sliding glass walls or temporary partitions.

    Attributes:
        type: Partition type identifier
        height: Height of the partition
        area: Surface area of the partition
        floatingPartition: Whether partition is floating (not touching floor/ceiling)
        object_ids: Unique object identifiers
        start_point: Starting point of the partition line
        end_point: Ending point of the partition line
    """
    type: str = attr()
    height: float = attr()
    area: float = attr()
    floatingPartition: bool = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    start_point: "Point3D" = element()
    end_point: "Point3D" = element()


class Zones(BaseModel):
    """Container for zone list.

    Attributes:
        zone: List of thermal zones
    """
    zone: List["Zone"] = element(tag="Zone")


class Zone(BaseModel):
    """A thermal zone - the smallest thermal node in the building model.

    Represents a single zone (room, office, space) with uniform thermal conditions,
    containing surfaces that form its boundaries.

    Attributes:
        parentZoneHandle: Reference to parent zone if hierarchical
        inheritedZoneHandle: Reference to inherited thermal properties
        planExtrusion: Extrusion method from plan geometry
        innerSurfaceMode: Mode for inner surface heat transfer
        body: 3D geometry of the zone
        light_sensor_one: Primary daylighting sensor location
        light_sensor_two: Secondary daylighting sensor location
        label_position: Position for zone label display
        polygon: 2D floor plan polygon
        inner_surface_body: Internal surfaces/partitions in the zone
    """
    parentZoneHandle: str = attr()
    inheritedZoneHandle: str = attr()
    planExtrusion: str = attr()
    innerSurfaceMode: str = attr()
    body: "Body" = element()
    light_sensor_one: "LightSensorOne" = element()
    light_sensor_two: "LightSensorTwo" = element()
    label_position: "Point3D" = element()
    polygon: Optional["Polygon"] = element(default=None)
    inner_surface_body: Optional["InnerSurfaceBody"] = element()


class ProfileBody(BaseModel):
    """Body created from a profile with extrusion properties.

    Represents geometry created by extruding a profile polygon with specified properties.

    Attributes:
        elementSlope: Slope angle of elements
        roofOverlap: Roof overlap dimension
        body: The 3D body geometry
    """
    elementSlope: float = attr()
    roofOverlap: float = attr()
    body: "Body" = element()


class Perimeter(BaseModel):
    """Perimeter boundary definition.

    Attributes:
        polygon: Polygon defining the perimeter
    """
    polygon: "Polygon" = element()


class BaseProfileBody(BaseModel):
    """Base profile for building geometry extrusion.

    Attributes:
        profile_body: The profile body definition
    """
    profile_body: "ProfileBody" = element()


class Polygon(BaseModel):
    """A 2D polygon defining boundary geometry.

    Represents a closed polygon path defining floor plans, surface boundaries, or openings.

    Attributes:
        auxiliaryType: Type classification for the polygon
        object_ids: Unique object identifiers
        vertices: List of 3D vertices forming the polygon
        polygon_holes: Holes within this polygon (for complex shapes)
    """
    auxiliaryType: str = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    vertices: Optional["Vertices"] = element(default=None)
    polygon_holes: Optional["PolygonHoles"] = element()


class PolygonHoles(BaseModel):
    """Container for polygon hole list.

    Attributes:
        polygon_hole: List of holes in the polygon
    """
    polygon_hole: List["PolygonHole"] = element(tag="PolygonHole")


class PolygonHole(BaseModel):
    """A hole within a polygon (for complex shapes).

    Represents cutouts or holes in a polygonal boundary.

    Attributes:
        object_ids: Unique object identifiers
        vertices: Vertices of the hole polygon
    """
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    vertices: "Vertices" = element()


class LightSensorOne(BaseModel):
    """First daylighting sensor location in a zone.

    Defines the primary point where daylighting levels are calculated.

    Attributes:
        index: Sensor index/identifier
        point_3d: 3D coordinates of the sensor location
    """
    index: int = attr()
    point_3d: str = element()


class LightSensorTwo(BaseModel):
    """Second daylighting sensor location in a zone.

    Defines the secondary point where daylighting levels are calculated.

    Attributes:
        index: Sensor index/identifier
        point_3d: 3D coordinates of the sensor location
    """
    index: int = attr()
    point_3d: str = element()


class InnerSurfaceBody(BaseModel):
    """Internal surfaces within a zone.

    Attributes:
        body: The inner surface body geometry
    """
    body: "Body" = element()


class BookmarkBuildings(BaseModel):
    """Bookmark references for building navigation.

    Attributes:
        numberOfBuildings: Number of bookmarked buildings
    """
    numberOfBuildings: int = attr()


class ConstructionLines(BaseModel):
    """Container for construction line list.

    Attributes:
        construction_line: List of construction lines
    """
    construction_line: List["ConstructionLine"] = element(tag="ConstructionLine")


class ConstructionLine(BaseModel):
    """A construction or reference line for building modeling.

    Represents auxiliary geometry for design reference.

    Attributes:
        line: The line geometry
        planes: Planes associated with this line
    """
    line: "Line" = element()
    planes: "CPlanes" = element()


class CPlanes(BaseModel):
    """Container for construction plane list.

    Attributes:
        polygon: List of polygons defining planes
    """
    polygon: List["Polygon"] = element(tag="Polygon")


class Planes(BaseModel):
    """Container for work plane list.

    Attributes:
        plane: List of work planes
    """
    plane: List["Plane"] = element(tag="Plane")


class Plane(BaseModel):
    """A single work plane used in building modeling.

    Attributes:
        type: Plane type identifier
        polygon: Polygon defining the plane boundaries
    """
    type: int = attr()
    polygon: "Polygon" = element()


class AssemblyInstances(BaseModel):
    """Container for assembly instance list.

    Attributes:
        assembly_instance: List of placed assembly instances
    """
    assembly_instance: List["AssemblyInstance"] = element(tag="AssemblyInstance")


class AssemblyInstance(BaseModel):
    """An instance of an assembly placed in the building.

    Represents a placed, possibly transformed copy of an assembly definition.

    Attributes:
        assemblyHandle: Reference to the assembly definition
        reflected: Whether assembly is reflected/mirrored
        active: Whether this instance is active
        object_ids: Unique object identifiers
        assembly_instance_transformation_matrix: Transformation matrix for position/rotation
        attributes: Key attributes for the instance
    """
    assemblyHandle: int = attr()
    reflected: int = attr()
    active: int = attr()
    object_ids: Annotated["ObjectIDs", Field(default_factory=ObjectIDs)] = element()
    assembly_instance_transformation_matrix: "AssemblyInstanceTransformationMatrix" = (
        element()
    )
    attributes: Optional["KeyAttributes"] = element()


class AssemblyInstanceTransformationMatrix(BaseModel):
    """Transformation matrix for assembly instance positioning.

    Attributes:
        matrix: The 4x4 transformation matrix rows
    """
    matrix: "Matrix" = element()


class Matrix(BaseModel):
    """A transformation or other matrix.

    Attributes:
        matrix_row: Rows of the matrix
    """
    matrix_row: List[str] = element(tag="MatrixRow")


class ProfileOutlines(BaseModel):
    """Container for profile outline list.

    Attributes:
        profile_outline: List of building profile outlines
    """
    profile_outline: List["ProfileOutline"] = element(tag="ProfileOutline")


class ProfileOutline(BaseModel):
    """A profile outline of the building for visualization.

    Attributes:
        body: The outline body geometry
    """
    body: "Body" = element()


class VoidBodies(BaseModel):
    """Container for void body list.

    Attributes:
        void_body: List of void bodies (atria, internal voids)
    """
    void_body: List["VoidBody"] = element(tag="VoidBody")


class VoidBody(BaseModel):
    """An internal void (atrium, internal courtyard, etc.).

    Represents empty space within a building.

    Attributes:
        profile_body: The void profile body
    """
    profile_body: "ProfileBody" = element()


class VoidPerimeterList(BaseModel):
    """Container for void perimeter polygon list.

    Attributes:
        polygon: List of void perimeter polygons
    """
    polygon: List["Polygon"] = element(tag="Polygon")


class CFDFans(BaseModel):
    """Container for CFD fan list.

    Attributes:
        cfd_fan: List of CFD fans for computational fluid dynamics
    """
    cfd_fan: List["CFDFan"] = element(tag="CFDFan")


class CFDFan(BaseModel):
    """A CFD fan component for computational fluid dynamics analysis.

    Attributes:
        component_block: The component block representing the fan
    """
    component_block: "ComponentBlock" = element()


class CFDBoundary(BaseModel):
    """CFD boundary condition definition.

    Defines boundary conditions for computational fluid dynamics analysis.

    Attributes:
        type: Boundary type identifier
        polygon: Boundary polygon geometry
        cfd_boundary_settings: Boundary condition parameters
        minimum_refinement_region_point: Minimum point of refinement region
        maximum_refinement_region_point: Maximum point of refinement region
        cfd_boundary_component_list: Components associated with boundary
    """
    type: str = attr()
    polygon: "Polygon" = element()
    cfd_boundary_settings: "CFDBoundarySettings" = element()
    minimum_refinement_region_point: "Point3D" = element()
    maximum_refinement_region_point: "Point3D" = element()
    cfd_boundary_component_list: Optional[None] = element(default=None)


class CFDSegmentList(BaseModel):
    """Container for CFD boundary segments.

    Attributes:
        cfd_boundary: CFD boundary definition
    """
    cfd_boundary: "CFDBoundary" = element()


class CFDBoundarySettings(BaseModel):
    """Boundary condition parameters for CFD analysis.

    Defines thermal, flow, and mesh parameters for CFD simulations.

    Attributes:
        temperature: Boundary temperature (K)
        flow_rate: Mass flow rate
        x_direction_discharge_angle: Discharge angle in X direction
        y_direction_discharge_angle: Discharge angle in Y direction
        multi_way_diffuser_discharge_angle: Multi-way diffuser angle
        two_way_diffuser_discharge_direction: Two-way diffuser direction
        minimum_discharge_velocity: Minimum discharge velocity
        actual_discharge_velocity: Actual discharge velocity
        heat_flux: Heat flux (W/m²)
        pressure: Pressure (Pa)
        pressure_type: Pressure type identifier
        moisture_source: Moisture source rate
        contaminant_source: Contaminant source concentration
        relative_humidity: Relative humidity (%)
        non_ortho_element_width: Non-orthogonal element width
        non_ortho_element_height: Non-orthogonal element height
        non_ortho_face_offset: Non-orthogonal face offset
        non_ortho_element_x_spacing: X-direction element spacing
        non_ortho_element_y_spacing: Y-direction element spacing
        non_ortho_element_x_edge_offset: X-edge offset
        non_ortho_element_y_edge_offset: Y-edge offset
        DiffuserElementDimension: Diffuser element dimension
        RefinementRegionDistance: Refinement region distance
        RefinementRegionLevel: Refinement region refinement level
    """
    temperature: float = attr()
    flow_rate: float = attr()
    x_direction_discharge_angle: float = attr()
    y_direction_discharge_angle: float = attr()
    multi_way_diffuser_discharge_angle: float = attr()
    two_way_diffuser_discharge_direction: int = attr()
    minimum_discharge_velocity: float = attr()
    actual_discharge_velocity: float = attr()
    heat_flux: float = attr()
    pressure: float = attr()
    pressure_type: int = attr()
    moisture_source: float = attr()
    contaminant_source: float = attr()
    relative_humidity: float = attr()
    non_ortho_element_width: float = attr()
    non_ortho_element_height: float = attr()
    non_ortho_face_offset: float = attr()
    non_ortho_element_x_spacing: float = attr()
    non_ortho_element_y_spacing: float = attr()
    non_ortho_element_x_edge_offset: float = attr()
    non_ortho_element_y_edge_offset: float = attr()
    DiffuserElementDimension: float
    RefinementRegionDistance: float
    RefinementRegionLevel: int
