import React, { useState } from 'react'
import { Stage, Layer, Rect } from 'react-konva'
import type { Table } from '../types'

export function LayoutCanvas() {
    const [tables, setTables] = useState<Table[]>([])
    const [selectedTable, setSelectedTable] = useState<Table | null>(null)

    const updateTableProperty = (property: keyof Table, value: number) => {
        if (!selectedTable) return
        const updatedTable = { ...selectedTable, [property]: value }
        setSelectedTable(updatedTable)
        setTables(tables.map(t => t.id == selectedTable.id ? updatedTable : t))
    }

    const handleTableClick = (table: Table) => {
        setSelectedTable(table)
    }
    const handleClick = (e: any) => {
        const stage = e.target.getStage()
        if (!stage) return
    
        const pos = stage.getPointerPosition()
        if (!pos) return
    
        const newTable = {
            id: Date.now().toString(),
            x: pos.x - 25,
            y: pos.y - 25,
            width: 50,
            height: 50
        }
    
        setTables([...tables, newTable])
    }

    return (
        <div className="flex">
            <div className="flex-1">
                <Stage width={800} height={600} onClick={handleClick}>
                    <Layer>
                    {tables.map(table => (
                        <Rect
                        key={table.id}
                        x={table.x}
                        y={table.y}
                        width={table.width}
                        height={table.height}
                        fill={selectedTable?.id == table.id ? 'blue' : 'gray'}//change color when selected
                        onClick={() => handleTableClick(table)}
                        />
                    ))}
                    </Layer>
                </Stage>
            </div>
            <div className="w-80 bg-gray-100 p-4">
                {selectedTable ? (
                    <div>
                        <label>X Position</label>
                        <input
                            type="number"
                            value={selectedTable.x}
                            onChange={(e) => updateTableProperty('x', Number(e.target.value))}
                        />
                    </div>
                ) : (
                    <p>Select a table</p>
                )}
            </div>
        </div>
    )
}