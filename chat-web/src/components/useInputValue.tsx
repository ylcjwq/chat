import { useState, useCallback, ChangeEvent } from "react";

// 自定义 Hook，用于管理输入框的值
function useInputValue(initialValue: any) {
  // 使用 state 存储输入框的值
  const [value, setValue] = useState(initialValue);

  // 创建一个更新输入框值的函数
  const handleChange = useCallback((event: ChangeEvent<HTMLInputElement>) => {
    setValue(event.target.value);
  }, []);

  // 返回当前的值和更新值的函数
  return [value, handleChange, setValue];
}

export default useInputValue;
