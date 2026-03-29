import uuid

from sqlalchemy import select, update

from module_llm.llm_run.entity.do.run_do import LlmRun
from module_llm.llm_run.entity.do.run_event_do import LlmRunEvent
from module_llm.llm_run.entity.vo.run_vo import RunDetailModel, RunEventModel, RunStatusUpdateModel


class RunDao:
    @staticmethod
    async def list_runs(
        query_db,
        session_id: str | None = None,
        status: str | None = None,
        provider_id: str | None = None,
        agent_id: str | None = None,
        model_code: str | None = None,
        failure_stage: str | None = None,
        failure_category: str | None = None,
    ):
        query = select(LlmRun).where(LlmRun.del_flag == '0')
        if session_id:
            query = query.where(LlmRun.session_id == session_id)
        if status:
            query = query.where(LlmRun.status == status)
        if provider_id:
            query = query.where(LlmRun.provider_id == provider_id)
        if agent_id:
            query = query.where(LlmRun.agent_id == agent_id)
        if model_code:
            query = query.where(LlmRun.model_code == model_code)
        if failure_stage:
            query = query.where(LlmRun.failure_stage == failure_stage)
        if failure_category:
            query = query.where(LlmRun.failure_category == failure_category)
        result = (await query_db.execute(query.order_by(LlmRun.create_time.desc()))).scalars().all()
        return [
            RunDetailModel(
                run_id=item.run_id,
                session_id=item.session_id,
                agent_id=item.agent_id,
                provider_id=item.provider_id,
                model_code=item.model_code,
                status=item.status,
                input_summary=item.input_summary,
                output_summary=item.output_summary,
                failure_stage=item.failure_stage,
                failure_category=item.failure_category,
                used_memory=item.used_memory,
                used_tool=item.used_tool,
                cost_summary=item.cost_summary,
            )
            for item in result
        ]

    @staticmethod
    async def get_run_detail(query_db, run_id: str):
        item = (await query_db.execute(select(LlmRun).where(LlmRun.run_id == run_id))).scalars().first()
        if not item or item.del_flag != '0':
            return None
        return RunDetailModel(
            run_id=item.run_id,
            session_id=item.session_id,
            agent_id=item.agent_id,
            provider_id=item.provider_id,
            model_code=item.model_code,
            status=item.status,
            input_summary=item.input_summary,
            output_summary=item.output_summary,
            failure_stage=item.failure_stage,
            failure_category=item.failure_category,
            used_memory=item.used_memory,
            used_tool=item.used_tool,
            cost_summary=item.cost_summary,
        )

    @staticmethod
    async def list_run_events(query_db, run_id: str):
        result = (
            await query_db.execute(
                select(LlmRunEvent)
                .where(LlmRunEvent.run_id == run_id, LlmRunEvent.del_flag == '0')
                .order_by(LlmRunEvent.seq_no.asc())
            )
        ).scalars().all()
        return [
            RunEventModel(
                event_id=item.event_id,
                run_id=item.run_id,
                seq_no=item.seq_no,
                event_type=item.event_type,
                event_payload=item.event_payload,
            )
            for item in result
        ]

    @staticmethod
    async def update_run_status(query_db, run_id: str, data: RunStatusUpdateModel):
        run = (await query_db.execute(select(LlmRun).where(LlmRun.run_id == run_id))).scalars().first()
        if not run or run.del_flag != '0':
            return None
        await query_db.execute(
            update(LlmRun)
            .where(LlmRun.run_id == run_id)
            .values(
                status=data.status,
                output_summary=data.output_summary,
                failure_stage=data.failure_stage,
                failure_category=data.failure_category,
                cost_summary=data.cost_summary,
                used_memory=data.used_memory,
                used_tool=data.used_tool,
            )
        )
        existing_events = (
            await query_db.execute(
                select(LlmRunEvent).where(LlmRunEvent.run_id == run_id, LlmRunEvent.del_flag == '0')
            )
        ).scalars().all()
        next_seq = max([item.seq_no for item in existing_events], default=0) + 1
        event = LlmRunEvent(
            event_id=str(uuid.uuid4()),
            run_id=run_id,
            seq_no=next_seq,
            event_type=data.event_type or f'run.{data.status}',
            event_payload=data.event_payload,
        )
        query_db.add(event)
        return {
            'run_id': run_id,
            'status': data.status,
            'event_id': event.event_id,
        }

    @staticmethod
    async def cancel_run(query_db, run_id: str):
        run = (await query_db.execute(select(LlmRun).where(LlmRun.run_id == run_id))).scalars().first()
        if not run or run.del_flag != '0':
            return None

        await query_db.execute(
            update(LlmRun)
            .where(LlmRun.run_id == run_id)
            .values(status='cancelled')
        )

        existing_events = (
            await query_db.execute(
                select(LlmRunEvent).where(LlmRunEvent.run_id == run_id, LlmRunEvent.del_flag == '0')
            )
        ).scalars().all()
        next_seq = max([item.seq_no for item in existing_events], default=0) + 1
        event = LlmRunEvent(
            event_id=str(uuid.uuid4()),
            run_id=run_id,
            seq_no=next_seq,
            event_type='run.cancelled',
            event_payload='{"status":"cancelled"}',
        )
        query_db.add(event)
        return {
            'run_id': run_id,
            'status': 'cancelled',
            'event_id': event.event_id,
        }
