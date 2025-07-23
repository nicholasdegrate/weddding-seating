import { z } from 'zod'
import { getApi } from '@/config/api.ts'

enum TableShape {
  ROUND = 'round',
  SQUARE = 'square',
  OVAL = 'oval',
  TRIANGLE = 'triangle',
}

const table = z.object({
  id: z.string(),
  name: z.string(),
  y: z.number(),
  x: z.number(),
  height: z.number(),
  width: z.number(),
  shape: z.nativeEnum(TableShape),
})

export type Table = z.infer<typeof table>

export async function getTablesByEvent(eventId: string) {
  const result = await getApi({
    url: `/events/${eventId}/tables`,
    resultSchema: table.array(),
  })

  if (!result.success) {
    return []
  }

  return result.data
}
