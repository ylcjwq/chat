import React from "react";
import ReactDOM from "react-dom/client";
import { RouterProvider } from "react-router";
import router from "@/routers";
import "@/styles/index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <RouterProvider router = {router}/>
  </React.StrictMode>
);
