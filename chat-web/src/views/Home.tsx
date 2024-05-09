import React, { useState } from "react";
import {
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
  AccountBookOutlined,
} from "@ant-design/icons";
import { Layout, Menu, theme, Tooltip } from "antd";
import SendMessageBar from "@/components/SendMessageBar";
import { postQuestion, getUseToken, getChatToken } from "@/api/request";
import {
  createUserContent,
  createRobotContent,
} from "@/components/ContentMessage";
import "@/styles/content.css";

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
    const main = document.querySelector(".content_container") as Element;
    createUserContent("问", value, main);
    // 这里可以添加发送消息的逻辑
    const robot = createRobotContent(main);
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
      const jsonChunks = text.split("data: "); // 处理单条流包含多个data的情况
      jsonChunks.forEach((message) => {
        if (message.trim() !== "") {
          try {
            const parsed = JSON.parse(message);
            const content = parsed.content;
            if (content === undefined) {
              return;
            }
            setRespMsg((prevRespMsg) => prevRespMsg + content);
            robot.append(content);
          } catch (error) {
            console.error("这似乎不是一个json字符串", message, error);
          }
        }
      });
    }
    robot.over();
  };

  const createUseToken = async () => {
    const data = await getUseToken();
    const data2 = await getChatToken();
    console.log(data);
    console.log(data2);
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
        <Header style={{ background: colorBgContainer }} className="header">
          <Tooltip title="24小时内用量">
            <AccountBookOutlined
              style={{ color: "rgba(0,0,0,.45)", fontSize: 20, marginLeft: 10 }}
              onClick={() => createUseToken()}
            />
          </Tooltip>
          <div className="logo">
            <span>🐕Chat-GPT🐕</span>
          </div>
        </Header>
        <Content style={{ margin: "10px 10px 0" }}>
          <div
            className="content_container"
            style={{
              padding: 20,
              height: contentHeight,
              borderRadius: borderRadiusLG,
              overflowY: "auto",
              scrollbarWidth: "none",
            }}
          ></div>
        </Content>
        <Footer style={{ textAlign: "center" }}>
          <SendMessageBar
            onSendMessage={sendMessage}
            onResize={(e: any) => handleFooterResize(e.height)}
          />
        </Footer>
      </Layout>
    </Layout>
  );
};

export default Home;
