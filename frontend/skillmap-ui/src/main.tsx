import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import Jobs from "./Jobs.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Jobs />
  </StrictMode>
);
