import ollama
import json
import os
import json2html


def translate_text_to_thai(text: str) -> str:
    """Translate English text to Thai using Ollama"""
    try:
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": "you are a translator system that translate security report from english to thai, check the meaning and tonality, return thai only"
                },
                {
                    "role": "user",
                    "content": f"Translate the following text to thai: {text}"
                }
            ],
            options={
                "temperature": 0.1,
                "num_predict": 500,
            }
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Return original if translation fails


def translate_event_to_thai(event: dict) -> dict:
    """Translate a single event's fields to Thai"""
    translated = event.copy()
    
    # Translate specific fields
    if "event_type" in event:
        translated["event_type"] = translate_text_to_thai(event["event_type"])
    
    if "description" in event:
        translated["description"] = translate_text_to_thai(event["description"])
    
    # Risk level translation
    risk_translation = {
        "low": "ต่ำ",
        "medium": "กลาง", 
        "high": "สูง"
    }
    if "risk_level" in event:
        translated["risk_level"] = risk_translation.get(event["risk_level"], event["risk_level"])
    
    return translated


def translate_json_report(input_json: str, output_json: str):
    """Translate entire JSON report to Thai"""
    print(f"\nTranslating JSON to Thai...")
    
    with open(input_json, "r") as f:
        events = json.load(f)
    
    translated_events = []
    total = len(events)
    
    for i, event in enumerate(events, 1):
        print(f"  Translating event {i}/{total}...", end=" ")
        translated = translate_event_to_thai(event)
        translated_events.append(translated)
        print("Done")
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(translated_events, f, indent=2, ensure_ascii=False)
    
    print(f"Thai JSON saved: {output_json}")
    return translated_events


def translate_html_report(input_json: str, output_html: str):
    """Generate Thai HTML report from translated JSON"""
    print(f"\nGenerating Thai HTML report...")
    
    with open(input_json, "r", encoding="utf-8") as f:
        events = json.load(f)
    
    html_table = json2html.convert(events)
    
    # Add Thai language meta and title
    html_content = f"""
    <html>
        <head>
            <meta charset='UTF-8'>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>รายงานการวิเคราะห์เหตุการณ์</title>
            <style>
                body {{ font-family: 'Sarabun', 'Tahoma', sans-serif; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
            </style>
        </head>
        <body>
            <h1>รายงานการวิเคราะห์เหตุการณ์</h1>
            {html_table}
        </body>
    </html>
    """
    
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Thai HTML saved: {output_html}")
    
    
if __name__ == "__main__":
    from p_config import *
    translate_json_report(OUTPUT_JSON, "./reports/report_th.json")
    