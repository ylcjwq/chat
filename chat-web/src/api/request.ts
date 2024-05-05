export const postQuestion = (question: string) => {
  const url = "http://127.0.0.1:8000/stream";
  const bodyData = { question: question };

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bodyData),
  });
};
