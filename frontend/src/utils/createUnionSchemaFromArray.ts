import { Primitive, z } from 'zod';

export function createUnionSchemaFromArray<T extends Primitive>(arr: [T, ...T[]] | readonly [T, ...T[]]) {
  const [firstItem, ...restItems] = arr;
  return restItems.reduce(
    (acc: z.ZodUnion<[z.ZodLiteral<T>, ...z.ZodLiteral<T>[]]> | z.ZodLiteral<T>, currentValue: T) => {
      return acc.or(z.literal(currentValue)) as z.ZodUnion<[z.ZodLiteral<T>, ...z.ZodLiteral<T>[]]>;
    },
    z.literal(firstItem) as z.ZodLiteral<T>,
  );
}
