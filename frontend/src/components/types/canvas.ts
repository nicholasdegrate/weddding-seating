export type TableShape = 'rectangle' | 'circle' | 'oval' | 'triangle'

export type Table = {
  id: string
  x: number
  y: number
  width: number
  height: number
  shape: TableShape
  selected: boolean
}

export type ToolSettings = {
  shape: TableShape
  width: number
  height: number
} 