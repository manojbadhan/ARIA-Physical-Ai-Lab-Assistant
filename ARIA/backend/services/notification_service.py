import logging
log = logging.getLogger("aria.notify")

def notify_faculty(message):
    """Placeholder hook: wire to email/Telegram later. Currently logs only."""
    log.info("Faculty notice: %s", message)
