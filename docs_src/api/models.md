# Models

Complete auto-generated API documentation for all DesignBuilder Schema Pydantic models.
Each class includes full type hints, field definitions, and inheritance information.

## Core Models

Building geometry, thermal zones, surfaces, and structural components.

::: db_schema.core
    options:
      members:
        - dsbXML
        - Site
        - Buildings
        - Building
        - BuildingBlocks
        - BuildingBlock
        - Zones
        - Zone
        - Body
        - Surfaces
        - Surface
        - Openings
        - Opening
        - Adjacencies
        - Adjacency
        - Polygon

## HVAC Network

::: db_schema.hvac.network
    options:
      members:
        - HVACNetwork
        - HVACLoops
        - HVACLoop
        - DemandSubLoop
        - SupplySubLoop
        - HVACZoneGroups
        - HVACZoneGroup
        - HVACConnections
        - HVACConnection

## HVAC Components

::: db_schema.hvac.components
    options:
      members:
        - NoTypeHVACComponent
        - HVACComponent
        - HVACComponents
        - AirHandlingUnit
        - Chiller
        - Pump
        - Boiler
        - Splitter
        - Mixer
        - SetpointManager
