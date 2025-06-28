from src.pptxjinja import Template

context = {
    "variables": {
        "project": "Dreamlead",
        "logo": "./templates/logo-dreamlead.png"
    },
    "collections": {
        "tickets": {
            "rows": [
                {"key": "JIRA-101", "summary": "Login faalt op mobiel"},
                {"key": "JIRA-102", "summary": "Kleuren inconsistent op iOS"},
                {"key": "JIRA-103", "summary": "Nog een ticket"},
            ]
        }
    },
    "split": {
        "tickets": {
            "type": "fixed",
            "max_per_slide": 2
        }
    }
}

Template("./templates/demo_template.pptx").render(context).save("./output/result.pptx")
print("Done generating presentation.")
