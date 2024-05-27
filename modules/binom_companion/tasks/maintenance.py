from loguru import logger

from datetime import datetime, timedelta, timezone

from libs.modules.AppContext import AppContext
from libs.modules.components import ScheduledTasks
from ..service import LeadRecordService

scheduled_tasks = ScheduledTasks()


# cleanup for old lead records
@scheduled_tasks.schedule_task(
    seconds=60,
    start_date=datetime.now() + timedelta(seconds=10)
)
async def old_lead_records_cleanup(
        ctx: AppContext,
        lead_record_ttl=60 * 30
):
    now = datetime.now(timezone.utc)

    query = await LeadRecordService().filter_queryable(
        time__lte=now - timedelta(seconds=lead_record_ttl)
    )
    num_deleted = await query.delete()

    logger.debug(f'Deleted {num_deleted} LeadRecords')