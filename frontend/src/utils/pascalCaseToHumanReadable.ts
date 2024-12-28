export const pascalCaseToHumanReadable = (input: string): string => {
  const readableString = input.replace(/([a-z])([A-Z])|([A-Z])([A-Z][a-z])/g, '$1$3 $2$4');
  return readableString.charAt(0).toUpperCase() + readableString.slice(1).toLowerCase();
};
