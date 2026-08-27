#!/usr/bin/env python3
"""
Generate a 2D Obsidian Canvas (.canvas) from surveyed OKF v0.2 symbols.
"""
import argparse
import json
import sys
from pathlib import Path

def build_canvas(stages, output_path: Path):
    """
    stages: list of dicts, each representing a column/stage:
      {
        "title": "Stage Name",
        "color": "1".."6",
        "nodes": [
          {"id": "node-1", "title": "Card Title", "text": "Card markdown content", "color": "1"}
        ]
      }
    """
    nodes = []
    edges = []
    
    x_start = -850
    col_width = 340
    col_gap = 70
    
    prev_col_nodes = []
    
    for col_idx, stage in enumerate(stages):
        x = x_start + col_idx * (col_width + col_gap)
        y = 100
        current_col_nodes = []
        
        for node_idx, item in enumerate(stage.get("nodes", [])):
            node_id = item.get("id", f"node-{col_idx}-{node_idx}")
            card = {
                "id": node_id,
                "type": "text",
                "x": x,
                "y": y,
                "width": col_width,
                "height": item.get("height", 280),
                "color": item.get("color", stage.get("color", "5")),
                "text": f"### {item.get('title', 'Component')}\n\n{item.get('text', '')}"
            }
            nodes.append(card)
            current_col_nodes.append(node_id)
            y += item.get("height", 280) + 40
            
        # Connect previous column to current column
        if prev_col_nodes and current_col_nodes:
            edges.append({
                "id": f"edge-{col_idx}",
                "fromNode": prev_col_nodes[0],
                "fromSide": "right",
                "toNode": current_col_nodes[0],
                "toSide": "left",
                "label": stage.get("edge_label", "flow")
            })
            
        prev_col_nodes = current_col_nodes

    canvas_json = {"nodes": nodes, "edges": edges}
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(canvas_json, indent=2), encoding="utf-8")
    print(f"Canvas successfully written to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate 2D Obsidian Canvas")
    parser.add_argument("--output", type=Path, default=Path("Architecture.canvas"), help="Output canvas path")
    args = parser.parse_args()
    print("Canvas builder ready. Pass custom stage data programmatically or through templates.")
