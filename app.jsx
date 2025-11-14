import React, { useState } from "react";

export default function App() {
  const [story, setStory] = useState("");
  const [image, setImage] = useState(null);
  const [reference, setReference] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const onFile = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = () => setImage(reader.result); // data URL
    reader.readAsDataURL(f);
  };

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/generate_title", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          story_text: story,
          image_base64: image,
          reference_title: reference,
        }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: String(err) });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 720, margin: "40px auto", fontFamily: "system-ui" }}>
      <h1>Contextual Story Title Generator</h1>
      <form onSubmit={submit}>
        <label>Story Text</label>
        <textarea rows={6} value={story} onChange={e => setStory(e.target.value)} style={{ width: "100%" }} />
        <label>Image (optional)</label>
        <input type="file" accept="image/*" onChange={onFile} />
        <label>Reference Title (optional)</label>
        <input type="text" value={reference} onChange={e => setReference(e.target.value)} style={{ width: "100%" }} />
        <button type="submit" disabled={loading} style={{ marginTop: 12 }}>
          {loading ? "Generating..." : "Generate Title"}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: 20, padding: 12, border: "1px solid #ddd", borderRadius: 8 }}>
          {result.error ? (
            <p style={{ color: "crimson" }}>{result.error}</p>
          ) : (
            <>
              <p><b>Generated Title:</b> {result.generated_title || "—"}</p>
              <p><b>BERTScore (F1):</b> {result.bertscore ? result.bertscore.toFixed(4) : "—"}</p>
              {result.bertscore != null && (
                <p style={{ color: result.bertscore >= 0.85 ? "green" : "orange" }}>
                  {result.bertscore >= 0.85 ? "Pass: ≥ 0.85" : "Below 0.85"}
                </p>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
