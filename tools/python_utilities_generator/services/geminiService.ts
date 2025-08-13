import { GoogleGenAI, Type } from "@google/genai";
import type { GeneratedFile } from "../types";

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  throw new Error("API_KEY environment variable not set.");
}

const ai = new GoogleGenAI({ apiKey: API_KEY });

const PYTHON_PACKAGE_SCHEMA = {
  type: Type.OBJECT,
  properties: {
    files: {
      type: Type.ARRAY,
      description: "An array of generated files for the Python package.",
      items: {
        type: Type.OBJECT,
        properties: {
          fileName: {
            type: Type.STRING,
            description: "The name of the file, e.g., 'main.py', 'README.md', 'config.json'."
          },
          fileContent: {
            type: Type.STRING,
            description: "The complete, raw content of the file."
          }
        },
        required: ["fileName", "fileContent"]
      }
    }
  },
  required: ["files"]
};

export const enhanceUserPrompt = async (userQuery: string, model: string): Promise<string> => {
    const enhancementPrompt = `
        You are an expert prompt engineer. Your task is to take a user's rough idea for a Python utility and refine it into a detailed, clear, and effective prompt for a code-generation AI.

        The code-generation AI has the following strict constraints:
        1.  **Standard Libraries Only:** It can ONLY use standard Python 3.8+ libraries (e.g., os, sys, json, re, argparse, http.server, xml.etree.ElementTree, ast). It CANNOT use any third-party packages that require 'pip install'. Do not suggest libraries like 'requests', 'beautifulsoup4', 'pandas', or 'numpy'.
        2.  **Modularity:** It is designed to create a logical multi-file structure (1-5 files).
        3.  **README is a Must:** It must always generate a 'README.md' file.
        4.  **Self-Contained:** The final output should be a complete, runnable package.

        **Your Goal:**
        Rewrite the user's query to be more explicit and structured. Expand on the user's idea, consider potential edge cases, and clarify requirements to help the code-generation AI produce a high-quality result that adheres to its constraints.

        **Example:**
        -   **User's Query:** "make a file crawler"
        -   **Your Enhanced Prompt:** "Create a Python script that recursively crawls a directory specified by a command-line argument. For each file found, log its path and size to a file named 'crawl_log.txt'. The script should handle errors gracefully, such as permission errors when accessing directories. Include a 'main.py' for the logic and a 'README.md' explaining how to run it (e.g., 'python main.py --directory /path/to/start')."

        **User's Query to Enhance:**
        "${userQuery}"

        **Instructions:**
        -   Directly output ONLY the enhanced prompt text.
        -   Do NOT include any explanations, introductory phrases like "Here is the enhanced prompt:", or markdown formatting.
        -   Ensure your enhanced prompt respects all the constraints of the code-generation AI.
    `;

    try {
        const response = await ai.models.generateContent({
            model,
            contents: enhancementPrompt,
        });

        return response.text.trim();
    } catch (error: any) {
        console.error("Error enhancing prompt:", error);
        throw new Error(`Failed to enhance prompt: ${error.message}`);
    }
};


export const generatePythonPackage = async (userQuery: string, model: string): Promise<GeneratedFile[]> => {
  const masterPrompt = `
    You are an expert Python developer specializing in creating modular, self-contained utility scripts. 
    Your task is to take a user's request and generate a complete, production-ready Python package with 1-5 files.
    
    **Constraints and Rules:**
    1.  **Standard Libraries Only:** You MUST use only standard Python 3.8+ libraries (e.g., os, sys, json, re, argparse, http.server, xml.etree.ElementTree, ast). Do NOT use or import any third-party/external packages that require 'pip install'.
    2.  **Modularity:** Design a logical multi-file structure. Each file must have a distinct and clear purpose.
    3.  **Robust Code:** The generated code must be clean, well-commented, and include robust error handling (e.g., try-except blocks, input validation).
    4.  **Complete README:** Always generate a 'README.md' file that explains the utility's purpose, the file structure, and provides clear, copy-pastable instructions on how to run it.
    5.  **Strict JSON Output:** Your entire response MUST be a single JSON object that strictly adheres to the provided schema. Do not include any introductory text, explanations, code block markers (like '''json'''), or anything outside of the main JSON object.

    **User Request:**
    "${userQuery}"

    **Your Step-by-Step Process:**
    1.  **Deconstruct Request:** Analyze the user's goal. Identify core functionality, required inputs/outputs, potential edge cases, and necessary configuration.
    2.  **Design File Structure:** Plan a modular structure of 1-5 files. Name them logically (e.g., 'main.py', 'utils.py', 'config.json', 'README.md').
    3.  **Synthesize Code & Content:** Write the full content for each planned file, following all constraints.
    4.  **Package into JSON:** Assemble the file names and their content into the final JSON structure as specified by the schema.
    `;

  try {
    const response = await ai.models.generateContent({
      model,
      contents: masterPrompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: PYTHON_PACKAGE_SCHEMA,
      },
    });
    
    // The response.text is expected to be a stringified JSON object matching the schema.
    const jsonString = response.text.trim();
    const parsedOutput = JSON.parse(jsonString);

    if (parsedOutput && Array.isArray(parsedOutput.files)) {
      // Sort files to have README first if it exists
      return parsedOutput.files.sort((a: GeneratedFile, b: GeneratedFile) => {
        if (a.fileName.toLowerCase() === 'readme.md') return -1;
        if (b.fileName.toLowerCase() === 'readme.md') return 1;
        if (a.fileName.toLowerCase() === 'main.py') return -1;
        if (b.fileName.toLowerCase() === 'main.py') return 1;
        return a.fileName.localeCompare(b.fileName);
      });
    } else {
      throw new Error("Invalid response structure from API.");
    }

  } catch (error: any) {
    console.error("Error generating Python package:", error);
    if (error.message.includes("JSON")) {
      throw new Error("The AI returned an invalid data format. Please try again.");
    }
    throw new Error(`Failed to generate package: ${error.message}`);
  }
};