import React, { useState } from 'react'
import { Stage, Layer, Rect } from 'react-konva'
import type { Table } from '../types'

export function LayoutCanvas() {
  const [tables, setTables] = useState<Table[]>([])

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
    <div className="h-screen">
      <Stage width={800} height={600} onClick={handleClick}>
        <Layer>
          {tables.map(table => (
            <Rect
              key={table.id}
              x={table.x}
              y={table.y}
              width={50}
              height={50}
              fill="gray"
            />
          ))}
        </Layer>
      </Stage>
    </div>
  )
}