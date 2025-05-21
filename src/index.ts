import * as path from "path";
import { readAllExcelFiles, readAllExcelFilesRaw } from "./utils/excel";
import { ChatDialog, ChatMessage } from "./types";
import * as fs from "fs";

function groupAndDepuplicate(allRows: any[]): ChatDialog {
  const dialogMap: ChatDialog = {};
  const dedupSet = new Set<string>();
  for (const row of allRows) {
    // 1. 生成对话id
    const dialogId = `${row["好友WechatId"]}`;
    // 2. 生成去重key
    const dedupKey = `${dialogId}_${row["发送人"]}_${row["消息内容"]}_${row["聊天时间"]}`;
    if (dedupSet.has(dedupKey)) {
      continue;
    }
    dedupSet.add(dedupKey);

    // 3. 组装消息
    const msg = {
      sender: row["发送人"],
      content: row["消息内容"],
      time: row["聊天时间"],
      selfName: row["微信昵称"],
    };

    // 4. 分组
    if (!dialogMap[dialogId]) {
      dialogMap[dialogId] = [];
    }
    dialogMap[dialogId].push(msg);
  }

  // 5. 每一组都按时间顺序排序，并去掉time字段
  for (const dialogId in dialogMap) {
    const arr = dialogMap[dialogId] as Array<{
      sender: string;
      content: string;
      time: string;
      selfName: string;
    }>;
    arr.sort((a, b) => new Date(a.time).getTime() - new Date(b.time).getTime());
    dialogMap[dialogId] = arr.map(({ sender, content, selfName }) => {
      const role = sender === selfName ? "客服" : "客户";
      return { [role]: content };
    });
  }

  return dialogMap;
}

async function main() {
  const dirPath = path.join(__dirname, "../excels");
  const allRows = readAllExcelFilesRaw(dirPath);
  const dialogMap = groupAndDepuplicate(allRows);

  console.log(`客户总数：${Object.keys(dialogMap).length}`);

  const outputDir = path.join(__dirname, "../output");
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
  }
  const timestamp = new Date().toISOString().replace(/[-:T]/g, "").slice(0, 12);
  const outputPath = path.join(outputDir, `output_${timestamp}.json`);
  fs.writeFileSync(outputPath, JSON.stringify(dialogMap, null, 2), "utf-8");
  console.log(`输出已保存至${outputPath}`);
}

main();
