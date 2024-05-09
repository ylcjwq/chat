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

export const getUseToken = () => {
  const url = `http://${import.meta.env.VITE_FETCH_URL}:8000/getUseToken`;

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json(); // 将响应体解析为JSON
  });
};

export const getChatToken = () => {
  const url = `http://${import.meta.env.VITE_FETCH_URL}:8000/getChatToken`;

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json(); // 将响应体解析为JSON
  });
};
