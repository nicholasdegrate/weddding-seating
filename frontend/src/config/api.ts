import type { z } from 'zod'
import { env } from '@/env.ts'
import { result } from '@/lib/result.ts'
import { getIdToken } from '@/config/firebase.ts'

type ApiParams<T extends z.ZodType<any, any, any>> = {
  url: string
  resultSchema: T
  config?: RequestInit
}

export async function getApi<T extends z.ZodType<any, any, any>>(
  args: ApiParams<T>,
): Promise<z.SafeParseReturnType<T, T>> {
  const token = await result(getIdToken())

  if (!token.success) {
    throw new Error(`Failed ID token`)
  }

  const resp = await result(
    fetch(env.API_BASE_URL + args.url, {
      method: 'GET',
      ...args.config,
      headers: {
        ...args.config?.headers,
        'Content-Type': 'application/json',
        Authorization: `Bearer: ${token.data}`,
      },
    }),
  )

  if (!resp.success || !resp.data.ok) {
    throw new Error(`Failed response API fetch`)
  }

  const data = await result(resp.data.json())
  if (!data.success) {
    throw new Error(`Failed response data`)
  }

  return args.resultSchema.safeParse(data)
}
