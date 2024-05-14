/**
 * 问答接口
 * @param question 问题
 * @param model 模型
 * @returns
 */
export const postQuestion = (question: string, model: string) => {
  const url = `http://${import.meta.env.VITE_FETCH_URL}:8000/stream`;
  const bodyData = { question: question, model: model };

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bodyData),
  });
};

/**
 * 图片生成接口
 * @param question 问题
 * @returns
 */
export const postImage = (question: string) => {
  const url = `http://${import.meta.env.VITE_FETCH_URL}:8000/getImage`;
  const bodyData = { question: question };

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(bodyData),
  });
};

/**
 * 查询24小时token用量
 * @returns
 */
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

/**
 * 查询总token用量
 * @returns
 */
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

/**
 * 清空上下文
 * @returns
 */
export const cleanHistory = () => {
  const url = `http://${import.meta.env.VITE_FETCH_URL}:8000/cleanHistory`;

  return fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
};
