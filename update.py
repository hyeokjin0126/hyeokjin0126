import json
from datetime import datetime, timedelta, timezone
import os

class ProfileCardGenerator:
    def __init__(self, data_path="info.json"):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"{data_path} 파일을 찾을 수 없습니다.")
            
        with open(data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        
        # 설정값
        self.width = 880  
        self.line_height = 26
        self.section_margin = 50
        self.exp_item_height = 32
        self.vertical_padding = 55
        self._analyze_data()

    def _analyze_data(self):
        # AGE
        birth = datetime.strptime(self.data['birth'], "%Y.%m.%d")
        today = datetime.now()
        self.age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        
        # EXPERIENCE
        self.exp_list = []
        for exp in self.data['experience']:
            is_present = exp['quit'].startswith("0000")
            period = f"{exp['start']} ~ {'Present' if is_present else exp['quit']}"
            self.exp_list.append({
                "company": exp['company'],
                "period": period
            })

    def generate(self, output_path="card.svg"):
        achieve_inner_h = len(self.data['achievements']) * self.line_height
        cert_inner_h = len(self.data['certifications']) * self.line_height
        exp_inner_h = len(self.exp_list) * self.exp_item_height
        
        # section
        achieve_total_h = achieve_inner_h + 30 + self.section_margin
        cert_total_h = cert_inner_h + 30 + self.section_margin
        exp_total_h = exp_inner_h + 30
        
        # header
        header_area_h = 135 
        total_content_h = header_area_h + achieve_total_h + cert_total_h + exp_total_h
        total_height = total_content_h + (self.vertical_padding * 2)

        svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.width}" height="{total_height}" viewBox="0 0 {self.width} {total_height}" xmlns="http://www.w3.org/2000/svg">
    <rect width="{self.width}" height="{total_height}" fill="#ffffff" stroke="none"/>
    
    <style>
        .base {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; fill: #000000; }}
        .name {{ font-size: 38px; font-weight: 800; text-transform: uppercase; }}
        .section-title {{ font-size: 19px; font-weight: 800; text-transform: uppercase; }}
        .label {{ font-size: 15px; font-weight: 800; }}
        .value {{ font-size: 15px; font-weight: 400; }}
        .bold-text {{ font-weight: 800; }}
        .line {{ stroke: #000000; stroke-width: 1.5; }}

        @media (prefers-color-scheme: dark) {{
            rect {{ fill: #0d1117; }}
            .base {{ fill: #ffffff; }}
            .line {{ stroke: #ffffff; }}
        }}
    </style>

    <g transform="translate(40, {self.vertical_padding})">
        <text y="0" class="base name">{self.data['names']['ko']} / {self.data['names']['en']}</text>
        <g transform="translate(0, 50)">
            <text y="0" class="base label">AGE<tspan font-weight="400" xml:space="preserve">  {self.age} ({self.data['birth']})</tspan></text>
            <text y="28" class="base label">EMAIL<tspan font-weight="400" xml:space="preserve">  {self.data['contact']['email']}</tspan></text>
            <text y="56" class="base label">LAST UPDATED<tspan font-weight="400" xml:space="preserve">  {datetime.now(timezone(timedelta(hours=9))).strftime("%Y.%m.%d %H:%M:%S")} (aactions-bot)</tspan></text>
        </g>
    </g>

    <line x1="40" y1="{self.vertical_padding + 130}" x2="{self.width-40}" y2="{self.vertical_padding + 130}" class="line"/>

    <g transform="translate(40, {self.vertical_padding + 175})">
        <g>
            <text y="0" class="base section-title">ACHIEVEMENTS</text>
            {"".join([f'<text y="{35 + i*self.line_height}" class="base value"><tspan class="bold-text">{a["date"]}</tspan><tspan xml:space="preserve">  -  </tspan>{a["title"]}</text>' for i, a in enumerate(self.data['achievements'])])}
        </g>

        <g transform="translate(0, {achieve_total_h})">
            <text y="0" class="base section-title">CERTIFICATIONS</text>
            {"".join([f'<text y="{35 + i*self.line_height}" class="base value"><tspan class="bold-text">{c["date"]}</tspan><tspan xml:space="preserve">  -  </tspan>{c["name"]}</text>' for i, c in enumerate(self.data['certifications'])])}
        </g>
        
        <g transform="translate(0, {achieve_total_h + cert_total_h})">
            <text y="0" class="base section-title">EXPERIENCE</text>
            {"".join([f'<text y="{35 + i*self.exp_item_height}" class="base value"><tspan class="bold-text">{e["company"]}</tspan><tspan xml:space="preserve">  -  </tspan>{e["period"]}</text>' for i, e in enumerate(self.exp_list)])}
        </g>
    </g>
</svg>'''

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)

if __name__ == "__main__":
    ProfileCardGenerator().generate()
