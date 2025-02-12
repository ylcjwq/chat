import React, { useState } from "react";
import { AccountBookOutlined } from "@ant-design/icons";
import { Layout, Menu, theme, Tooltip, Spin, Modal } from "antd";
import SendMessageBar from "@/components/SendMessageBar";
import {
  postQuestion,
  postImage,
  getChatToken,
  cleanHistory,
} from "@/api/request";
import {
  createUserContent,
  createRobotContent,
} from "@/components/ContentMessage";
import "@/styles/content.css";

const { Header, Content, Footer, Sider } = Layout;

const items = ["gpt-3.5-turbo", "gpt-4o-mini", "图片生成", "deepseek-reasoner"].map(
  (item, index) => ({
    key: String(index + 1),
    label: item,
  })
);

const Home: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const [footerHeight, setFooterHeight] = useState<number>(0);
  const [gptModel, setGptModel] = useState<string>("gpt-3.5-turbo");
  const [spinning, setSpinning] = useState<boolean>(false);

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
    if (gptModel === "图片生成") {
      const resp = await postImage(value);
      const data = await resp.json();
      console.log(data.data[0].url);
      robot.append(data.data[0].url);
    } else {
      const resp = await postQuestion(value, gptModel);
      
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
              robot.append(content);
            } catch (error) {
              console.error("这似乎不是一个json字符串", message, error);
            }
          }
        });
      }
      robot.over();
    }
  };

  const createUseToken = async () => {
    setSpinning(true);
    const data = await getChatToken();
    setSpinning(false);
    Modal.info({
      title: "当前token使用情况",
      content: (
        <div>
          <p>token总数：{data.balanceTotal}</p>
          <p>总使用量：{data.balanceUsed}</p>
          <p>剩余token：{data.balanceTotal - data.balanceUsed}</p>
        </div>
      ),
      onOk() {},
    });
  };

  const changeModel = async (value: string) => {
    setGptModel(value);
    setSpinning(true);
    await cleanHistory();
    setSpinning(false);
  };

  return (
    <Layout>
      <Spin spinning={spinning} fullscreen />
      <Sider breakpoint="lg" collapsedWidth="0">
        <div className="demo-logo-vertical" />
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={["1"]}
          items={items}
          onSelect={(e: any) =>
            changeModel(items.filter((item) => item.key === e.key)[0].label)
          }
        />
      </Sider>
      <Layout>
        <Header style={{ background: colorBgContainer }} className="header">
          <Tooltip title="查询用量">
            <AccountBookOutlined
              style={{ color: "rgba(0,0,0,.45)", fontSize: 20, marginLeft: 10 }}
              onClick={() => createUseToken()}
            />
          </Tooltip>
          <div className="logo">
            <span>小金-AI</span>
          </div>
        </Header>
        <Content style={{ margin: "10px 10px 0", height: contentHeight, overflowY: "auto" }}>
          <div
            className="content_container"
            style={{
              padding: 20,
              // height: contentHeight,
              borderRadius: borderRadiusLG,  
              overflowY: "auto",
              scrollbarWidth: "none",
            }}
          >
          </div>
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
