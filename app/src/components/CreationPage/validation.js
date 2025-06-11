/**
 * Validation rules for node properties.
 * Each property type has a rule and validation function.
 */
export const PROPERTY_VALIDATIONS = {
  // ✅ Custom Signal properties
  Frequencies: {
    type: "text",
    regex: /^\s*\d+(\.\d+)?(\s*,\s*\d+(\.\d+)?)*\s*$/,
    errorMessage: "Must be comma-separated numbers (e.g., 10, 20, 40)",
  },
  Amplitudes: {
    type: "text",
    regex: /^\s*\d+(\.\d+)?(\s*,\s*\d+(\.\d+)?)*\s*$/,
    errorMessage: "Must be comma-separated numbers (e.g., 20, 15, 10)",
  },

  // ✅ Range inputs (e.g., "0.1-4, 4-8")
  "Berger Bands": {
    type: "text", // Changed to text to accept string format
    regex: /^\s*\d+(\.\d+)?\s*-\s*\d+(\.\d+)?(\s*,\s*\d+(\.\d+)?\s*-\s*\d+(\.\d+)?)*\s*$/,
    errorMessage: "Must be in format 'min-max, min-max' (e.g., '0.1-4, 4-8, 8-12')",
  },

  // ✅ Numeric values (float)
  Frequency: {
    type: "number",
    min: 0,
    max: 1000,
    unit: "Hz",
    errorMessage: "Must be between 0 and 1000 Hz",
  },
  "Clock Frequency": {
    type: "number",
    min: 0,
    max: 1000000,
    unit: "Hz",
    errorMessage: "Must be between 0 and 1000000 Hz",
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
    min: -9999999,
    max: 9999999,
    errorMessage: "Must be between -9999999 and 9999999",
  },
  "Upper Bound": {
    type: "number",
    min: -9999999,
    max: 9999999,
    errorMessage: "Must be between -9999999 and 9999999",
  },
  Weights: {
    type: "text",
    regex: /^\[(\d+(\.\d+)?)(,\s*\d+(\.\d+)?)*\]$/,
    errorMessage: "Must be in array format (e.g., [1, 1, 1])",
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
    errorMessage: "Must be true or false",
  },

  // ✅ Text-based values
  "File Path": {
    type: "text",
    regex: /^(\/?[\w\-. ]+)+\.\w{2,4}$/,
    errorMessage: "Must be a valid file path (e.g., /data/file.txt)",
  },
  
  // ✅ EEG Dataset properties
  "Dataset Path": {
    type: "text",
    regex: /^(\/?[\w\-. ]+)+\.mat$/,
    errorMessage: "Must be a valid .mat file path (e.g., /data/eeg_data.mat)",
  },
  "Info File Path": {
    type: "text", 
    regex: /^(\/?[\w\-. ]+)+\.mat$/,
    errorMessage: "Must be a valid .mat file path (e.g., /data/eeg_info.mat)",
  },
  "Window Duration": {
    type: "number",
    min: 0.1,
    max: 60.0,
    unit: "s",
    errorMessage: "Must be between 0.1 and 60.0 seconds",
  },
  "Window Offset": {
    type: "number",
    min: 0.0,
    max: 30.0,
    unit: "s",
    errorMessage: "Must be between 0.0 and window duration seconds (up to 30.0s max)",
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
    case "text":
      if (rule.regex) {
        return rule.regex.test(value);
      }
      return true;
    case "number":
      const num = parseFloat(value);
      return !isNaN(num) && num >= rule.min && num <= rule.max;
    case "integer":
      const int = parseInt(value, 10);
      return Number.isInteger(int) && int >= rule.min && int <= rule.max;
    case "boolean":
      return typeof value === "boolean";
    case "dropdown":
      return rule.allowedValues.includes(value);
    default:
      return true;
  }
}
