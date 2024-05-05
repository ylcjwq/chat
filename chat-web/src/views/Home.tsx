import React, { useState } from "react";
import {
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
} from "@ant-design/icons";
import { Layout, Menu, theme } from "antd";
import SendMessageBar from "@/components/SendMessageBar";
import { postQuestion } from "@/api/request";

const { Header, Content, Footer, Sider } = Layout;

const items = [
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  UserOutlined,
].map((icon, index) => ({
  key: String(index + 1),
  icon: React.createElement(icon),
  label: `nav ${index + 1}`,
}));

const Home: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const [footerHeight, setFooterHeight] = useState<number>(0);
  const [respMsg, setRespMsg] = useState<string>("");

  // 动态计算content区域的高度
  const handleFooterResize = (height: number) => {
    setFooterHeight(height);
  };
  const viewportHeight = window.innerHeight;
  const contentHeight = viewportHeight - footerHeight - 144;

  const sendMessage = async (value: string) => {
    console.log(value);
    // 这里可以添加发送消息的逻辑
    const resp = await postQuestion(value);
    // 一部分一部分去读响应体
    const reader = resp.body!.getReader();
    const decoder = new TextDecoder(); // 文本解码器
    while (1) {
      const { done, value } = await reader.read();
      if (done) {
        // 读完了
        break;
      }
      const text = decoder.decode(value);
      // console.log(text);
      const jsonChunks = text.split("data: ");
      jsonChunks.forEach((message) => {
        if (message.trim() !== "") {
          console.log(message);
          if (message === "[DONE]") {
            return;
          }
          try {
            const parsed = JSON.parse(message);
            const content = parsed.choices[0].delta.content;
            if (content === undefined) {
              return;
            }
            console.log(content);

            setRespMsg((prevRespMsg) => prevRespMsg + content);
          } catch (error) {
            console.error(
              "Could not JSON parse stream message",
              message,
              error
            );
          }
        }
      });
    }
  };

  return (
    <Layout>
      <Sider breakpoint="lg" collapsedWidth="0">
        <div className="demo-logo-vertical" />
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={["4"]}
          items={items}
        />
      </Sider>
      <Layout>
        <Header style={{ padding: 0, background: colorBgContainer }} />
        <Content style={{ margin: "10px 10px 0" }}>
          <div
            style={{
              padding: 20,
              height: contentHeight,
              background: colorBgContainer,
              borderRadius: borderRadiusLG,
            }}
          >
            {respMsg}
          </div>
        </Content>
        <Footer style={{ textAlign: "center" }}>
          <SendMessageBar
            onSendMessage={sendMessage}
            onResize={(e) => handleFooterResize(e.height)}
          />
        </Footer>
      </Layout>
    </Layout>
  );
};

export default Home;
