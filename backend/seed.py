"""Seed the database with example data for demo/testing."""
import json
from datetime import datetime, timedelta, UTC

from sqlmodel import Session

from app.database import engine, create_db_and_tables
from app.models.user import User
from app.models.problem import Challenge, ChallengeCollaborator, CollaboratorRole, ChallengeStatus
from app.models.idea import Idea
from app.models.session import GreenlightSession, SessionStatus
from app.models.analysis import Analysis, AnalysisType
from app.models.comment import Comment
from app.models.approval import SessionApproval, GateType
from app.models.draft import IdeaDraft
from app.models.group import Team, TeamMember, GroupRole

create_db_and_tables()

with Session(engine) as s:
    # ── Users (real Clerk accounts) ──
    jesse = User(name="Jesse Henson", email="henson.jhenson.jesse@gmail.com", clerk_id="user_3AJuC4NoIHKo3Fg5ikwJWAConc5")
    alex = User(name="Alex Chen", email="alex@greenlight-test.com", clerk_id="user_3AK0CSWLKiDJEuFoxG5SfRAnAe2")
    jordan = User(name="Jordan Lee", email="jordan@greenlight-test.com", clerk_id="user_3AK0CRpfKYne8P1i0eyQcopqaQM")
    sam = User(name="Sam Rivera", email="sam@greenlight-test.com", clerk_id="user_3AK0CUAmmV9Cel8ptRuZOclIJZV")
    s.add_all([jesse, alex, jordan, sam])
    s.commit()
    s.refresh(jesse)
    s.refresh(alex)
    s.refresh(jordan)
    s.refresh(sam)

    # ── Team ──
    team = Team(name="Product Team")
    s.add(team)
    s.commit()
    s.refresh(team)

    s.add(TeamMember(group_id=team.id, user_id=jesse.id, role=GroupRole.owner))
    s.add(TeamMember(group_id=team.id, user_id=alex.id, role=GroupRole.member))
    s.add(TeamMember(group_id=team.id, user_id=jordan.id, role=GroupRole.member))
    s.add(TeamMember(group_id=team.id, user_id=sam.id, role=GroupRole.member))
    s.commit()

    # ═══════════════════════════════════════════════════════
    # Challenge 1 — Ideate phase (active, with ideas from multiple people)
    # ═══════════════════════════════════════════════════════
    c1 = Challenge(
        title="How might we reduce meeting fatigue?",
        description="Our team spends over 20 hours per week in meetings and it's crushing productivity. We need creative approaches to reduce meeting overhead while keeping everyone aligned.",
        created_by=jesse.id,
        group_id=team.id,
    )
    s.add(c1)
    s.commit()
    s.refresh(c1)

    s.add(ChallengeCollaborator(challenge_id=c1.id, user_id=jesse.id, role=CollaboratorRole.owner))
    s.add(ChallengeCollaborator(challenge_id=c1.id, user_id=alex.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c1.id, user_id=jordan.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c1.id, user_id=sam.id, role=CollaboratorRole.collaborator))
    session1 = GreenlightSession(challenge_id=c1.id, status=SessionStatus.ideate)
    s.add(session1)
    s.commit()
    s.refresh(session1)

    idea_c1_1 = Idea(challenge_id=c1.id, content="Replace all recurring meetings with async video updates — record a 2-min Loom instead", created_by=jesse.id)
    idea_c1_2 = Idea(challenge_id=c1.id, content="Meeting-free Wednesdays — no meetings allowed at all on Wednesdays, company-wide", created_by=alex.id)
    idea_c1_3 = Idea(challenge_id=c1.id, content="AI meeting bot that attends for you and sends a summary — you only join if action items involve you", created_by=jordan.id)
    idea_c1_4 = Idea(challenge_id=c1.id, content="15-minute hard cap on all meetings with a visible countdown timer everyone can see", created_by=sam.id)
    idea_c1_5 = Idea(challenge_id=c1.id, content="Walking meetings for 1:1s — get outside, no screens, just talk and walk", created_by=alex.id)
    s.add_all([idea_c1_1, idea_c1_2, idea_c1_3, idea_c1_4, idea_c1_5])
    s.commit()
    s.refresh(idea_c1_1)
    s.refresh(idea_c1_2)
    s.refresh(idea_c1_3)
    s.refresh(idea_c1_4)
    s.refresh(idea_c1_5)

    # Draft notes from different users
    s.add(IdeaDraft(
        idea_id=idea_c1_1.id, user_id=jesse.id,
        notes="Love the async angle — could combine with written summaries",
        want_pros_cons=True, want_feasibility=True, want_impact=False,
    ))
    s.add(IdeaDraft(
        idea_id=idea_c1_2.id, user_id=alex.id,
        notes="Simple and bold — would need exec buy-in",
        want_pros_cons=True, want_feasibility=False, want_impact=True,
    ))
    s.add(IdeaDraft(
        idea_id=idea_c1_3.id, user_id=jordan.id,
        notes="Technically ambitious but the ROI could be huge",
        want_pros_cons=True, want_feasibility=True, want_impact=True,
    ))

    # ═══════════════════════════════════════════════════════
    # Challenge 2 — Build phase (ideas submitted, team advancing)
    # ═══════════════════════════════════════════════════════
    c2 = Challenge(
        title="Improve our hiring pipeline speed",
        description="It takes us 45 days on average to go from first interview to offer. Candidates are dropping off. We need to cut this in half without sacrificing quality.",
        created_by=alex.id,
        group_id=team.id,
    )
    s.add(c2)
    s.commit()
    s.refresh(c2)

    s.add(ChallengeCollaborator(challenge_id=c2.id, user_id=jesse.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c2.id, user_id=alex.id, role=CollaboratorRole.owner))
    s.add(ChallengeCollaborator(challenge_id=c2.id, user_id=jordan.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c2.id, user_id=sam.id, role=CollaboratorRole.collaborator))
    session2 = GreenlightSession(challenge_id=c2.id, status=SessionStatus.build)
    s.add(session2)
    s.commit()
    s.refresh(session2)

    # All approved ideate->build gate
    s.add(SessionApproval(session_id=session2.id, user_id=jesse.id, gate=GateType.ideate_to_build))
    s.add(SessionApproval(session_id=session2.id, user_id=alex.id, gate=GateType.ideate_to_build))
    s.add(SessionApproval(session_id=session2.id, user_id=jordan.id, gate=GateType.ideate_to_build))
    s.add(SessionApproval(session_id=session2.id, user_id=sam.id, gate=GateType.ideate_to_build))

    idea_c2_1 = Idea(challenge_id=c2.id, content="Consolidate all interviews into a single 'super day' — 3 hours, meet everyone, decision by EOD", created_by=alex.id)
    idea_c2_2 = Idea(challenge_id=c2.id, content="Async take-home replaced with live pair programming — 45 min, immediate signal, no weekend homework", created_by=jesse.id)
    idea_c2_3 = Idea(challenge_id=c2.id, content="AI pre-screening that scores resumes and auto-schedules qualified candidates within 24 hours", created_by=sam.id)
    idea_c2_4 = Idea(challenge_id=c2.id, content="Yes, and — the super day could end with a team lunch so the candidate gets culture signal too", created_by=jordan.id)
    s.add_all([idea_c2_1, idea_c2_2, idea_c2_3, idea_c2_4])
    s.commit()
    s.refresh(idea_c2_1)
    s.refresh(idea_c2_2)
    s.refresh(idea_c2_3)
    s.refresh(idea_c2_4)

    # ═══════════════════════════════════════════════════════
    # Challenge 3 — Analysis complete (full demo with all data)
    # ═══════════════════════════════════════════════════════
    c3 = Challenge(
        title="Redesign the onboarding experience",
        description="New hires take 3 months to feel productive. We need ideas to compress onboarding and make the first week feel exciting, not overwhelming.",
        created_by=jordan.id,
        group_id=team.id,
    )
    s.add(c3)
    s.commit()
    s.refresh(c3)

    s.add(ChallengeCollaborator(challenge_id=c3.id, user_id=jesse.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c3.id, user_id=alex.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c3.id, user_id=jordan.id, role=CollaboratorRole.owner))
    s.add(ChallengeCollaborator(challenge_id=c3.id, user_id=sam.id, role=CollaboratorRole.collaborator))
    session3 = GreenlightSession(challenge_id=c3.id, status=SessionStatus.analysis_complete)
    s.add(session3)
    s.commit()
    s.refresh(session3)

    # All approved both gates
    for u in [jesse, alex, jordan, sam]:
        s.add(SessionApproval(session_id=session3.id, user_id=u.id, gate=GateType.ideate_to_build))
        s.add(SessionApproval(session_id=session3.id, user_id=u.id, gate=GateType.build_to_converge))

    idea1 = Idea(challenge_id=c3.id, content="Pair every new hire with a 'day one buddy' who walks them through their first real task together", created_by=jesse.id)
    idea2 = Idea(challenge_id=c3.id, content="Gamified onboarding quest — complete challenges to unlock access to tools, repos, and Slack channels", created_by=alex.id)
    idea3 = Idea(challenge_id=c3.id, content="Ship something on day one — have a tiny PR ready for them to modify, test, and deploy", created_by=jordan.id)
    s.add_all([idea1, idea2, idea3])
    s.commit()
    s.refresh(idea1)
    s.refresh(idea2)
    s.refresh(idea3)

    # ── Analyses for idea 1: Day One Buddy ──
    s.add(Analysis(idea_id=idea1.id, analysis_type=AnalysisType.pros_cons, content=json.dumps({
        "pros": [
            "Immediate human connection reduces first-day anxiety",
            "Knowledge transfer happens naturally through pairing",
            "Builds team relationships from day one",
        ],
        "cons": [
            "Buddy's productivity dips during onboarding week",
            "Quality depends on buddy's teaching skills",
            "May not scale well during large hiring waves",
        ],
        "stakeholder_impact": "Highly positive for new hires — they feel welcomed and productive faster. Moderate cost to buddies' existing workload."
    })))
    s.add(Analysis(idea_id=idea1.id, analysis_type=AnalysisType.feasibility, content=json.dumps({
        "score": 8, "logistics": "Easy to set up — just assign buddies from same team",
        "cost": "Low — only cost is buddy's time (~10 hrs/week for first week)",
        "time": "Can start immediately with next hire",
        "complexity": "Low — needs a buddy matching guide and a short training doc",
        "summary": "Highly feasible with minimal overhead"
    })))
    s.add(Analysis(idea_id=idea1.id, analysis_type=AnalysisType.impact, content=json.dumps({
        "score": 8, "team_impact": "Buddies develop mentoring skills; team bonds strengthen",
        "user_impact": "New hires feel supported and productive faster",
        "balance_assessment": "Strong positive impact across the board",
        "risks": "Risk of buddy burnout if they're assigned too frequently"
    })))

    # ── Analyses for idea 2: Gamified Quest ──
    s.add(Analysis(idea_id=idea2.id, analysis_type=AnalysisType.pros_cons, content=json.dumps({
        "pros": [
            "Makes onboarding feel fun and engaging",
            "Self-paced — new hires aren't blocked by others' schedules",
            "Progress is visible and measurable",
        ],
        "cons": [
            "Significant upfront development effort",
            "Needs ongoing maintenance as tools change",
            "Some people may find gamification patronizing",
        ],
        "stakeholder_impact": "Very engaging for new hires who enjoy game mechanics. Engineering team needs to build and maintain the platform."
    })))
    s.add(Analysis(idea_id=idea2.id, analysis_type=AnalysisType.feasibility, content=json.dumps({
        "score": 5, "logistics": "Need to build quest platform and integrate with existing tools",
        "cost": "Medium — 2-3 sprints of engineering effort upfront",
        "time": "2-3 months to build v1",
        "complexity": "Medium-high — integrations with Slack, GitHub, HR systems",
        "summary": "Requires meaningful investment but scales well"
    })))
    s.add(Analysis(idea_id=idea2.id, analysis_type=AnalysisType.impact, content=json.dumps({
        "score": 7, "team_impact": "Reduces ad-hoc onboarding questions; standardizes the experience",
        "user_impact": "New hires get a structured, self-guided experience",
        "balance_assessment": "Good long-term investment but high initial cost",
        "risks": "May become stale if not regularly updated with new content"
    })))

    # ── Analyses for idea 3: Ship on Day One ──
    s.add(Analysis(idea_id=idea3.id, analysis_type=AnalysisType.pros_cons, content=json.dumps({
        "pros": [
            "Incredible confidence boost — 'I shipped on my first day!'",
            "Forces dev environment setup to actually work",
            "Creates immediate sense of contribution",
        ],
        "cons": [
            "Requires maintaining a ready-to-go starter PR",
            "Might feel artificial if the change is too trivial",
            "Some roles don't have code to ship",
        ],
        "stakeholder_impact": "Hugely motivating for new engineers. Minimal impact on codebase. Forces the team to keep their setup docs current."
    })))
    s.add(Analysis(idea_id=idea3.id, analysis_type=AnalysisType.feasibility, content=json.dumps({
        "score": 7, "logistics": "Need a library of starter PRs maintained per team",
        "cost": "Low — small ongoing effort to maintain starter tasks",
        "time": "Can start within a week",
        "complexity": "Low-medium — needs CI/CD to support safe 'first deploy'",
        "summary": "Very doable with some prep work"
    })))
    s.add(Analysis(idea_id=idea3.id, analysis_type=AnalysisType.impact, content=json.dumps({
        "score": 9, "team_impact": "Team gets a real (small) contribution on day one",
        "user_impact": "New hire feels accomplished and part of the team immediately",
        "balance_assessment": "Highest impact-to-effort ratio of all ideas",
        "risks": "Risk of deployment issues causing a stressful first day if not well-prepared"
    })))

    # ── Summary ──
    s.add(Analysis(challenge_id=c3.id, analysis_type=AnalysisType.summary, content=json.dumps({
        "themes": ["Immediate contribution", "Human connection", "Self-paced learning", "Reducing anxiety"],
        "top_recommendations": [
            {"idea": "Ship something on day one", "why": "Highest impact with lowest effort — creates immediate sense of belonging and contribution"},
            {"idea": "Day one buddy system", "why": "Complements shipping by providing human support; easy to implement immediately"},
        ],
        "trade_offs": [
            "Ship-on-day-one requires maintained starter tasks but creates incredible first impressions",
            "Gamified quest has the best long-term scalability but highest upfront cost",
            "Buddy system is free but depends on individual buddy quality",
        ],
        "next_steps": [
            "Create 3 starter PRs (one per team) for the ship-on-day-one program",
            "Write a buddy matching guide and pilot with next 2 hires",
            "Evaluate gamified quest ROI after buddy + ship programs are running",
        ]
    })))

    # ── Comments on ideas (from multiple users) ──
    now = datetime.now(UTC)
    s.add(Comment(idea_id=idea3.id, content="This is brilliant — I wish I had this when I started. The dev setup alone took me 2 days.", created_by=alex.id, created_at=now - timedelta(hours=2)))
    s.add(Comment(idea_id=idea3.id, content="We could pre-configure their laptop image so the environment is ready to go on day one.", created_by=jesse.id, created_at=now - timedelta(hours=1, minutes=45)))
    s.add(Comment(idea_id=idea3.id, content="Yes! And we should have a celebration Slack message when they merge their first PR.", created_by=jordan.id, created_at=now - timedelta(hours=1, minutes=30)))
    s.add(Comment(idea_id=idea3.id, content="What about non-engineering roles though? We'd need a version of this for design, PM, etc.", created_by=sam.id, created_at=now - timedelta(hours=1)))

    s.add(Comment(idea_id=idea1.id, content="I was a buddy at my last company and it was the most rewarding thing I did all year.", created_by=sam.id, created_at=now - timedelta(hours=3)))
    s.add(Comment(idea_id=idea1.id, content="We should make sure buddies get recognition — maybe a small bonus or shoutout.", created_by=alex.id, created_at=now - timedelta(hours=2, minutes=30)))

    # ═══════════════════════════════════════════════════════
    # Challenge 4 — Empty, just started (by Sam)
    # ═══════════════════════════════════════════════════════
    c4 = Challenge(
        title="Boost team engagement for remote workers",
        description="Half our team is remote and they consistently score lower on engagement surveys. We need creative ideas to make remote teammates feel just as connected and valued as in-office folks.",
        created_by=sam.id,
        group_id=team.id,
    )
    s.add(c4)
    s.commit()
    s.refresh(c4)

    s.add(ChallengeCollaborator(challenge_id=c4.id, user_id=jesse.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c4.id, user_id=alex.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c4.id, user_id=jordan.id, role=CollaboratorRole.collaborator))
    s.add(ChallengeCollaborator(challenge_id=c4.id, user_id=sam.id, role=CollaboratorRole.owner))
    s.add(GreenlightSession(challenge_id=c4.id, status=SessionStatus.ideate))

    s.commit()
    print("Seeded: 4 users, 1 team, 4 challenges, 12 ideas, 10 analyses, 6 comments, 12 approvals, 3 drafts")
