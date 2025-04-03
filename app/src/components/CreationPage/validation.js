/**
 * Validation rules for node properties.
 * Each property type has a rule and validation function.
 */
export const PROPERTY_VALIDATIONS = {
  // ✅ Range inputs (e.g., "0.1-4, 4-8")
  "Berger Bands": {
    type: "array", // ✅ Now treated as an array of min-max pairs
    minValue: 0,
    maxValue: 1000,
    errorMessage: "Each value must be between 0 and 1000 Hz.",
  },

  // ✅ Numeric values (float)
  "Clock Frequency": {
    type: "number",
    min: 0,
    max: 1000,
    unit: "MHz",
    errorMessage: "Must be between 0 and 1000 MHz",
  },
  "Sampling Frequency": {
    type: "number",
    min: 0,
    max: 1000,
    unit: "Hz",
    errorMessage: "Must be between 0 and 1000 Hz",
  },
  "Lower Bound": {
    type: "number",
    min: -1000,
    max: 1000,
    errorMessage: "Must be between -1000 and 1000",
  },
  "Upper Bound": {
    type: "number",
    min: -1000,
    max: 1000,
    errorMessage: "Must be between -1000 and 1000",
  },

  // ✅ Integer values
  "Number of Samples": {
    type: "integer",
    min: 0,
    max: 1000000,
    errorMessage: "Must be a whole number between 0 and 1,000,000",
  },
  "Number of Channels": {
    type: "integer",
    min: 0,
    max: 256,
    errorMessage: "Must be a whole number between 0 and 256",
  },

  // ✅ Boolean values
  "Enable RTL Simulation": {
    type: "boolean",
  },
  "Enable RTL Power Estimation": {
    type: "boolean",
  },

  // ✅ Text-based values
  "File Path": {
    type: "text",
    regex: /^(\/?[\w\-. ]+)+\.\w{2,4}$/,
    errorMessage: "Must be a valid file path (e.g., /data/file.txt)",
  },
  "Model Weights": {
    type: "text",
    regex: /^(\/?[\w\-. ]+)+\.\w{2,4}$/,
    errorMessage: "Must be a valid file path (e.g., /models/weights.pth)",
  },
  "Storage Type": {
    type: "dropdown",
    allowedValues: [
      "Spin-Transfer Torque",
      "Phase-Change Memory",
      "Ferroelectric Field-Effect Transistor",
      "Resistive Random Access Memory",
    ],
    errorMessage: "Must select a valid storage type.",
  },
};

/**
 * Generic validation function that checks if an input is valid based on the schema.
 *
 * @param {string} key - The property name.
 * @param {any} value - The user-entered value.
 * @returns {boolean} - Whether the value is valid.
 */
export function validateProperty(key, value) {
  const rule = PROPERTY_VALIDATIONS[key];
  if (!rule) return true; // No validation rule → always valid

  switch (rule.type) {
    case "range":
      return rule.regex.test(value);
    case "number":
      const num = parseFloat(value);
      return !isNaN(num) && num >= rule.min && num <= rule.max;
    case "integer":
      const int = parseInt(value, 10);
      return Number.isInteger(int) && int >= rule.min && int <= rule.max;
    case "boolean":
      return typeof value === "boolean";
    case "text":
      if (rule.allowedValues) {
        return rule.allowedValues.includes(value);
      }
      return rule.regex.test(value);
    default:
      return true;
  }
}
