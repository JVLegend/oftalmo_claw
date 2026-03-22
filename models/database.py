"""Database connection, session management, and seed data."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, func
from config import settings


engine = create_async_engine(settings.database_url, echo=settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_demo_data()


async def get_db():
    async with async_session() as session:
        yield session


async def seed_demo_data():
    """Seed database with demo data if empty."""
    from models.doctor import Doctor
    from models.case import Case, CaseStatus, CaseUrgency, Specialty, Opinion
    from models.exam import ExamRecord
    from models.chat import ChatHistory  # noqa: F401 — ensures table is created
    from datetime import datetime, timedelta
    import random

    async with async_session() as session:
        count = await session.scalar(select(func.count()).select_from(Doctor))
        if count and count > 0:
            return  # Already seeded

        # --- Doctors ---
        doctors = [
            Doctor(
                name="Dr. Carlos Silva", email="carlos@oftalmo.dev", crm="CRM-SP 123456",
                specialty=Specialty.GENERAL, is_active=True, is_online=True, password_hash="demo",
            ),
            Doctor(
                name="Dra. Ana Oliveira", email="ana@oftalmo.dev", crm="CRM-SP 234567",
                specialty=Specialty.RETINA, is_active=True, is_online=True, password_hash="demo",
            ),
            Doctor(
                name="Dr. Roberto Costa", email="roberto@oftalmo.dev", crm="CRM-SP 345678",
                specialty=Specialty.GLAUCOMA, is_active=True, is_online=True, password_hash="demo",
            ),
            Doctor(
                name="Dra. Maria Santos", email="maria@oftalmo.dev", crm="CRM-SP 456789",
                specialty=Specialty.CORNEA, is_active=True, is_online=False, password_hash="demo",
            ),
            Doctor(
                name="Dr. Paulo Mendes", email="paulo@oftalmo.dev", crm="CRM-SP 567890",
                specialty=Specialty.RETINA, is_active=True, is_online=True, password_hash="demo",
            ),
        ]
        session.add_all(doctors)
        await session.flush()

        # --- Cases ---
        cases = [
            Case(
                case_number="#2847", patient_age=56, patient_gender="F",
                patient_history="HAS, DM2 há 10 anos",
                chief_complaint="Baixa visual progressiva OE há 3 meses",
                hypothesis="Edema macular diabético",
                exam_findings="OCT: aumento de espessura foveal OE (420um), cistos intrarretinianos",
                urgency=CaseUrgency.URGENT, status=CaseStatus.PENDING,
                specialty_requested=Specialty.RETINA,
                requested_by_id=doctors[0].id, assigned_to_id=doctors[1].id,
                created_at=datetime.utcnow() - timedelta(hours=2),
            ),
            Case(
                case_number="#2845", patient_age=68, patient_gender="M",
                patient_history="Glaucoma OD em tratamento há 5 anos",
                chief_complaint="Progressão de perda campimétrica apesar de PIO controlada",
                hypothesis="Glaucoma de pressão normal vs progressão",
                exam_findings="CV: defeito arciforme superior OD, MD -8.5dB. OCT RNFL: afinamento inferior",
                urgency=CaseUrgency.NORMAL, status=CaseStatus.IN_ANALYSIS,
                specialty_requested=Specialty.GLAUCOMA,
                requested_by_id=doctors[3].id, assigned_to_id=doctors[2].id,
                created_at=datetime.utcnow() - timedelta(hours=6),
            ),
            Case(
                case_number="#2843", patient_age=42, patient_gender="F",
                patient_history="Sem comorbidades. Usa lentes de contato há 15 anos",
                chief_complaint="Piora progressiva da visão com óculos",
                hypothesis="Ceratocone vs ectasia corneana",
                exam_findings="Topografia: Kmax 49.2D OD, I-S 2.1. Paquimetria: 468um",
                urgency=CaseUrgency.NORMAL, status=CaseStatus.PENDING,
                specialty_requested=Specialty.CORNEA,
                requested_by_id=doctors[4].id, assigned_to_id=doctors[3].id,
                created_at=datetime.utcnow() - timedelta(days=1),
            ),
        ]
        session.add_all(cases)
        await session.flush()

        # --- Opinions ---
        opinions = [
            Opinion(
                case_id=cases[0].id, doctor_id=doctors[1].id,
                diagnosis="Edema macular diabético centro-envolvente OE",
                recommendation="Iniciar anti-VEGF intravítreo (aflibercepte 2mg). Controle glicêmico rigoroso. Retorno com OCT em 4 semanas.",
                confidence=0.85, ai_assisted="N",
            ),
            Opinion(
                case_id=cases[1].id, doctor_id=doctors[2].id,
                diagnosis="Progressão glaucomatosa apesar de PIO alvo. Possível componente vascular.",
                recommendation="Considerar redução adicional da PIO (meta <14mmHg). Solicitar angio-OCT para avaliar perfusão peripapilar. Reavaliar em 3 meses.",
                confidence=0.7, ai_assisted="N",
            ),
            Opinion(
                case_id=cases[1].id, doctor_id=doctors[4].id,
                diagnosis="Concordo com progressão. Padrão de perda sugere dano axonal ativo.",
                recommendation="Adicionar brimonidina (neuroproteção). Considerar SLT se PIO não atingir meta com medicação.",
                confidence=0.75, ai_assisted="N",
            ),
        ]
        session.add_all(opinions)

        # --- Exam Records (6 months of data) ---
        exam_types = ["fundoscopia", "oct", "campimetria", "topografia", "biometria", "retinografia"]
        base_volumes = [90, 65, 46, 33, 28, 22]
        now = datetime.utcnow()

        for month_offset in range(6):
            month_date = now - timedelta(days=30 * (5 - month_offset))
            growth = 1 + (month_offset * 0.08)  # 8% growth per month
            for i, exam_type in enumerate(exam_types):
                volume = int(base_volumes[i] * growth)
                for j in range(volume):
                    day_offset = random.randint(0, 29)
                    score = round(random.gauss(88 + month_offset * 0.8, 4), 1)
                    score = max(60, min(100, score))
                    doctor = random.choice(doctors)
                    session.add(ExamRecord(
                        exam_type=exam_type,
                        patient_id=f"PAC-{random.randint(1000, 9999)}",
                        doctor_id=doctor.id,
                        eye=random.choice(["OD", "OS", "OU"]),
                        quality_score=score,
                        report_generated="Y" if random.random() > 0.1 else "N",
                        report_signed="Y" if random.random() > 0.2 else "N",
                        created_at=month_date + timedelta(days=day_offset, hours=random.randint(7, 18)),
                    ))

        await session.commit()
