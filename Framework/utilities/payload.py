class Payload:

    BLOCKS = {
        "blocks": []
    }

    DIVIDER = {
        "type": "divider"
    }

    PLAN_TEXT = {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "PLAIN TEXT",
            "emoji": True
        }
    }

    MARK_DOWN = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "MARK DOWN"
        }
    }

    CONTEXT_TEXT = {
        "type": "context",
        "elements": [
            {
                "type": "plain_text",
                "text": "CONTEXT TEXT",
                "emoji": True
            }
        ]
    }

