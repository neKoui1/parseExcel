import { ChatDialog } from "../types";
import * as fs from "fs";
import * as path from "path";
import * as xlsx from "xlsx";

/**
 * 读取目录下的所有excel文件
 * 返回所有原始数据的数组
 * @param dirPath
 * @returns
 */
export function readAllExcelFilesRaw(dirPath: string): any[] {
  const files = fs.readdirSync(dirPath);
  const excelFiles = files.filter(
    (file) => file.endsWith("xls") || file.endsWith("xlsx")
  );

  let allRows: any[] = [];
  for (const file of excelFiles) {
    const filePath = path.join(dirPath, file);
    const workbook = xlsx.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const rows = xlsx.utils.sheet_to_json(sheet);
    allRows = allRows.concat(rows);
  }
  return allRows;
}

/**
 * 读取指定目录下的所有Excel文件
 * 返回整理后的聊天记录
 */
export function readAllExcelFiles(dirPath: string): Promise<ChatDialog> {
  return Promise.resolve({});
}
