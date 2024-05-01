import React, { useState } from "react";
import {
  UploadOutlined,
  UserOutlined,
  VideoCameraOutlined,
  MessageOutlined,
} from "@ant-design/icons";
import { Layout, Menu, theme, Input, Tooltip, Space } from "antd";

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
  const handleFooterResize = (height: number) => {
    // 监听底部高度变化并重新赋值
    setFooterHeight(height);
  };
  const viewportHeight = window.innerHeight; // 获取视口高度
  const contentHeight = viewportHeight - footerHeight - 144; // 动态计算内容区域高度

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
            content
          </div>
        </Content>
        <Footer style={{ textAlign: "center" }}>
          <Space.Compact style={{ width: "100%", position: "relative" }}>
            <Input.TextArea
              style={{ padding: "0 24px 0 0" }}
              maxLength={2000}
              showCount
              autoSize={{ minRows: 1, maxRows: 3 }}
              onResize={(e) => handleFooterResize(e.height)}
              placeholder="请输入"
            />
            <div style={{ position: "absolute", right: 10, top: 6, zIndex: 1 }}>
              <Tooltip title="发送（回车）">
                <MessageOutlined
                  style={{ color: "rgba(0,0,0,.45)", fontSize: 20 }}
                  onClick={() => console.log("send")}
                />
              </Tooltip>
            </div>
          </Space.Compact>
        </Footer>
      </Layout>
    </Layout>
  );
};

export default Home;
