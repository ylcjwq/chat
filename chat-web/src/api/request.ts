export const postQuestion = (question: string) => {
  const url = `http://${import.meta.env.VITE_FETCH_URL}:8000/stream`;
  const bodyData = { question: question };

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bodyData),
  });
};
