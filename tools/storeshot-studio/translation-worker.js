import {env, pipeline} from "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.8.1/dist/transformers.min.js";

env.allowLocalModels = false;
env.backends.onnx.wasm.numThreads = 1;
env.backends.onnx.wasm.proxy = false;

self.onmessage = async ({data: {model, revision, texts, traditional, sourceLanguage = "en", targetLanguage}}) => {
  try {
    let convert;
    if (traditional) {
      const {Converter} = await import("https://cdn.jsdelivr.net/npm/opencc-js@1.0.5/dist/esm/cn2t.js");
      convert = Converter({from: "cn", to: "t"});
    }
    const translate = await pipeline("translation", model, {
      revision,
      device: "wasm",
      dtype: "q8",
      progress_callback(event) {
        if (event.status === "progress") {
          self.postMessage({progress: Math.round(event.progress)});
        }
      },
    });
    const results = [];
    const languages = targetLanguage ? {src_lang: sourceLanguage, tgt_lang: targetLanguage} : {};
    for (const [index, text] of texts.entries()) {
      self.postMessage({completed: index, total: texts.length});
      const maxNewTokens = Math.min(192, Math.max(16, Array.from(text.trim()).length * 3));
      const [output] = await translate(text, {...languages, max_new_tokens: maxNewTokens, num_beams: 3});
      const result = output?.translation_text?.trim();
      if (!result) throw new Error("Missing translation");
      results.push(convert ? convert(result) : result);
    }
    self.postMessage({results});
  } catch (error) {
    console.error("StoreShot translation failed", error);
    self.postMessage({error: true});
  }
};
