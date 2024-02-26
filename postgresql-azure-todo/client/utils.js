export function formDataToJson(formData) {
  const jsonData = {};
  formData.forEach((value, key) => {
    jsonData[key] = value;
  });
  return jsonData;
}
