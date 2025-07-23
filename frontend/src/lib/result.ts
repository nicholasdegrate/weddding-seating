type CommonResult<T> = {
  /**
   * Returns the result, assuming the result was successful
   * Throws if the result was an error
   */
  unwrap: () => T;

  /**
   * Returns the result, unless it was an error.
   * If it's an error, the provided default value is returned instead.
   */
  unwrap_or_default: (value: T) => T;
};
type SuccessfulResult<T> = CommonResult<T> & { success: true; data: T };
type FailedResult<T> = CommonResult<T> & {
  success: false;
  err: unknown;
};
export type Result<T> = SuccessfulResult<T> | FailedResult<T>;

/**
 * Utility function for initializing a successful a result
 */
export function success<T>(data: T): SuccessfulResult<T> {
  return {
    success: true,
    data,
    unwrap() {
      return data;
    },
    unwrap_or_default(_value: T) {
      return data;
    },
  };
}

/**
 * Utility function for initializing a successful a result
 */
export function failed<T>(err: unknown): FailedResult<T> {
  return {
    success: false,
    err,
    unwrap() {
      if (err == null) {
        throw new Error("Unexpected Error");
      }

      throw err;
    },
    unwrap_or_default(value: T) {
      return value;
    },
  };
}

/**
 * Utility function turning a promise into a result
 */
export async function result<T>(
  p: PromiseLike<T>
): Promise<Result<Awaited<T>>> {
  try {
    const data = await p;
    return success(data);
  } catch (err) {
    return failed(err);
  }
}