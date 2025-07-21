import { useState, useRef, useEffect } from 'react'
import { Stage, Layer, Rect, Circle, Ellipse, RegularPolygon, Transformer } from 'react-konva'
import type Konva from 'konva'
import type { Table, TableShape, ToolSettings } from '../types/canvas'

export function LayoutCanvas() {
  // Basic state
  const [tables, setTables] = useState<Table[]>([])
  const [selectedTable, setSelectedTable] = useState<Table | null>(null)
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 })
  const [isClient, setIsClient] = useState(false)
  const [toolSettings, setToolSettings] = useState<ToolSettings>({
    shape: 'rectangle',
    width: 50,
    height: 50
  })
  const [showGrid, setShowGrid] = useState(true)
  const [gridSize, setGridSize] = useState(20)
  
  // Refs
  const transformerRef = useRef<Konva.Transformer>(null)
  const stageRef = useRef<Konva.Stage>(null)

  // Client-side initialization and responsive canvas
  useEffect(() => {
    setIsClient(true)
    
    const updateDimensions = () => {
      setDimensions({
        width: window.innerWidth - 320, // Account for sidebar
        height: window.innerHeight
      })
    }
    
    updateDimensions()
    window.addEventListener('resize', updateDimensions)
    return () => window.removeEventListener('resize', updateDimensions)
  }, [])

  // Click-to-create functionality
  const handleStageClick = (e: Konva.KonvaEventObject<MouseEvent>) => {
    // Only create on empty space
    if (e.target === e.target.getStage()) {
      const stage = e.target.getStage()
      if (!stage) return
      
      const pointerPosition = stage.getPointerPosition()
      if (!pointerPosition) return
      
      const newTable: Table = {
        id: `table-${Date.now()}`,
        x: pointerPosition.x - (toolSettings.width / 2), // Center the table
        y: pointerPosition.y - (toolSettings.height / 2),
        width: toolSettings.width,
        height: toolSettings.height,
        shape: toolSettings.shape,
        selected: false
      }
      
      setTables([...tables, newTable])
    }
  }

  // Table selection
  const handleTableClick = (table: Table) => {
    setSelectedTable(table)
    setTables(tables.map((t: Table) => ({ 
      ...t, 
      selected: t.id === table.id 
    })))
  }

  // Drag functionality
  const handleTableDragEnd = (e: Konva.KonvaEventObject<DragEvent>, tableId: string) => {
    const updatedTables = tables.map((table: Table) =>
      table.id === tableId
        ? { ...table, x: e.target.x(), y: e.target.y() }
        : table
    )
    setTables(updatedTables)
    
    // Update selected table if it was the one dragged
    if (selectedTable?.id === tableId) {
      setSelectedTable({ ...selectedTable, x: e.target.x(), y: e.target.y() })
    }
  }

  // Transformer effect
  useEffect(() => {
    if (selectedTable && transformerRef.current) {
      const stage = stageRef.current
      if (stage) {
        const tableNode = stage.findOne(`#table-${selectedTable.id}`)
        if (tableNode) {
          transformerRef.current.nodes([tableNode])
          transformerRef.current.getLayer()?.batchDraw()
        }
      }
    }
  }, [selectedTable])

  // Property updates
  const updateTableProperties = (property: keyof Table, value: number) => {
    if (!selectedTable) return
    
    const updatedTable = { ...selectedTable, [property]: value }
    setSelectedTable(updatedTable)
    setTables(tables.map((table: Table) =>
      table.id === selectedTable.id ? updatedTable : table
    ))
  }

  // Delete functionality
  const deleteSelectedTable = () => {
    if (!selectedTable) return
    
    setTables(tables.filter((table: Table) => table.id !== selectedTable.id))
    setSelectedTable(null)
    
    // Clear transformer
    if (transformerRef.current) {
      transformerRef.current.nodes([])
      transformerRef.current.getLayer()?.batchDraw()
    }
  }

  // Render grid lines
  const renderGrid = () => {
    if (!showGrid) return []
    
    const lines = []
    
    // Vertical lines
    for (let x = 0; x <= dimensions.width; x += gridSize) {
      lines.push(
        <Rect
          key={`v-${x}`}
          x={x}
          y={0}
          width={2}
          height={dimensions.height}
          fill="#9ca3af"
          opacity={0.7}
        />
      )
    }
    
    // Horizontal lines
    for (let y = 0; y <= dimensions.height; y += gridSize) {
      lines.push(
        <Rect
          key={`h-${y}`}
          x={0}
          y={y}
          width={dimensions.width}
          height={2}
          fill="#9ca3af"
          opacity={0.7}
        />
      )
    }
    
    return lines
  }

  // Render table shape based on type
  const renderTableShape = (table: Table) => {
    const commonProps = {
      key: table.id,
      id: `table-${table.id}`,
      x: table.x,
      y: table.y,
      fill: table.selected ? '#3b82f6' : '#6b7280',
      stroke: table.selected ? '#1d4ed8' : '#374151',
      strokeWidth: table.selected ? 4 : 2,
      shadowColor: table.selected ? '#1d4ed8' : 'transparent',
      shadowBlur: table.selected ? 10 : 0,
      shadowOffset: table.selected ? { x: 2, y: 2 } : { x: 0, y: 0 },
      draggable: true,
      onClick: () => handleTableClick(table),
      onDragEnd: (e: Konva.KonvaEventObject<DragEvent>) => handleTableDragEnd(e, table.id)
    }

    switch (table.shape) {
      case 'circle':
        return (
          <Circle
            {...commonProps}
            radius={Math.min(table.width, table.height) / 2}
          />
        )
      case 'oval':
        return (
          <Ellipse
            {...commonProps}
            radiusX={table.width / 2}
            radiusY={table.height / 2}
          />
        )
      case 'triangle':
        return (
          <RegularPolygon
            {...commonProps}
            sides={3}
            radius={Math.min(table.width, table.height) / 2}
          />
        )
      default: // rectangle
        return (
          <Rect
            {...commonProps}
            width={table.width}
            height={table.height}
          />
        )
    }
  }

  if (!isClient) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>
  }

  return (
    <div className="flex h-screen">
      <div className="flex-1 relative">
        <Stage 
          ref={stageRef} 
          width={dimensions.width} 
          height={dimensions.height}
          onClick={handleStageClick}
        >
          {/* Background layer with grid */}
          <Layer>
            {/* Grid lines */}
            {renderGrid()}
          </Layer>
          {/* Tables layer */}
          <Layer>
            {tables.map((table) => renderTableShape(table))}
            {selectedTable && (
              <Transformer
                ref={transformerRef}
                boundBoxFunc={(oldBox, newBox) => newBox}
              />
            )}
          </Layer>
        </Stage>
      </div>
      
      <div className="w-80 bg-gray-100 p-4 border-l border-gray-200 overflow-y-auto">
        {/* Tools Section */}
        <div className="mb-6">
          <h2 className="text-lg font-semibold mb-4">Tools</h2>
          <div className="space-y-4">
            {/* Grid Controls */}
            <div className="border-b border-gray-200 pb-4">
              <h3 className="text-md font-medium text-gray-700 mb-3">Grid Settings</h3>
              <div className="space-y-3">
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    id="showGrid"
                    checked={showGrid}
                    onChange={(e) => setShowGrid(e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label htmlFor="showGrid" className="ml-2 block text-sm text-gray-700">
                    Show Grid
                  </label>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Grid Size
                  </label>
                  <input
                    type="number"
                    min="5"
                    max="100"
                    value={gridSize}
                    onChange={(e) => setGridSize(Number(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
            </div>

            {/* Table Creation Tools */}
            <div>
              <h3 className="text-md font-medium text-gray-700 mb-3">Table Creation</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Table Shape
                  </label>
                  <select
                    value={toolSettings.shape}
                    onChange={(e) => setToolSettings({ ...toolSettings, shape: e.target.value as TableShape })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="rectangle">Rectangle</option>
                    <option value="circle">Circle</option>
                    <option value="oval">Oval</option>
                    <option value="triangle">Triangle</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Width
                  </label>
                  <input
                    type="number"
                    value={toolSettings.width}
                    onChange={(e) => setToolSettings({ ...toolSettings, width: Number(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Height
                  </label>
                  <input
                    type="number"
                    value={toolSettings.height}
                    onChange={(e) => setToolSettings({ ...toolSettings, height: Number(e.target.value) })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div className="pt-2">
                  <p className="text-sm text-gray-600 mb-2">
                    Click on the canvas to add a new table with these settings
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Table Properties Section */}
        <div className="border-t border-gray-300 pt-6">
          <h2 className="text-lg font-semibold mb-4">Table Properties</h2>
          {selectedTable ? (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Shape
                </label>
                <select
                  value={selectedTable.shape}
                  onChange={(e) => {
                    const updatedTable = { ...selectedTable, shape: e.target.value as TableShape }
                    setSelectedTable(updatedTable)
                    setTables(tables.map((table: Table) =>
                      table.id === selectedTable.id ? updatedTable : table
                    ))
                  }}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="rectangle">Rectangle</option>
                  <option value="circle">Circle</option>
                  <option value="oval">Oval</option>
                  <option value="triangle">Triangle</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  X Position
                </label>
                <input
                  type="number"
                  value={Math.round(selectedTable.x)}
                  onChange={(e) => updateTableProperties('x', Number(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Y Position
                </label>
                <input
                  type="number"
                  value={Math.round(selectedTable.y)}
                  onChange={(e) => updateTableProperties('y', Number(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Width
                </label>
                <input
                  type="number"
                  value={selectedTable.width}
                  onChange={(e) => updateTableProperties('width', Number(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Height
                </label>
                <input
                  type="number"
                  value={selectedTable.height}
                  onChange={(e) => updateTableProperties('height', Number(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="pt-4 border-t border-gray-200">
                <button
                  onClick={deleteSelectedTable}
                  className="w-full px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 transition-colors"
                >
                  Delete Table
                </button>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">Click on a table to edit its properties</p>
          )}
        </div>
      </div>
    </div>
  )
} 