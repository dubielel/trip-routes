export declare type DeepNonNullable<T> = {
  [P in keyof T]: NonNullable<T[P]> extends object ? DeepNonNullable<NonNullable<T[P]>> : NonNullable<T[P]>;
};
