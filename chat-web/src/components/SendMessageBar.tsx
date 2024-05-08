import React from "react";
import { MessageOutlined } from "@ant-design/icons";
import { Input, Tooltip, Space, message } from "antd";
import useInputValue from "@/hooks/useInputValue";

// 发送消息栏组件接口
interface SendMessageBarProps {
  onSendMessage: (message: string) => void;
  onResize: (e: any) => void;
}

// 发送消息栏组件
const SendMessageBar: React.FC<SendMessageBarProps> = ({
  onSendMessage,
  onResize,
}) => {
  const [inputValue, handleInputChange, setInputValue] = useInputValue("");

  // 处理发送事件
  const sendMessage = (e: React.KeyboardEvent | React.MouseEvent) => {
    e.preventDefault();
    if (inputValue.trim() === "") {
      message.warning("请输入内容");
      return;
    }
    onSendMessage(inputValue);
    setInputValue("");
  };

  return (
    <Space.Compact style={{ width: "100%", position: "relative" }}>
      <Input.TextArea
        style={{ padding: "0 24px 0 0" }}
        maxLength={2000}
        showCount
        autoSize={{ minRows: 1, maxRows: 3 }}
        placeholder="请输入"
        value={inputValue}
        onChange={handleInputChange}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            sendMessage(e);
          }
        }}
        onResize={onResize}
      />
      <div style={{ position: "absolute", right: 10, top: 6, zIndex: 1 }}>
        <Tooltip title="发送（回车）">
          <MessageOutlined
            style={{ color: "rgba(0,0,0,.45)", fontSize: 20 }}
            onClick={(e) => sendMessage(e)}
          />
        </Tooltip>
      </div>
    </Space.Compact>
  );
};

export default SendMessageBar;
