export type SSEEvent = { event: string; data: unknown };

export async function* readSSE(res: Response): AsyncGenerator<SSEEvent> {
  const reader = res.body!.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += value;

    const parts = buffer.split("\n\n");
    buffer = parts.pop() ?? "";

    for (const part of parts) {
      const event = part.match(/^event: (.*)$/m)?.[1] ?? "message";
      const data = part.match(/^data: (.*)$/m)?.[1];
      if (data !== undefined) yield { event, data: JSON.parse(data) };
    }
  }
}
