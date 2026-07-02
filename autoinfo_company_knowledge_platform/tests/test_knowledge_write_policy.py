from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase


class TestKnowledgeWritePolicy(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dept_a = cls.env["knowledge.department"].create({"name": "Dept A"})
        cls.dept_b = cls.env["knowledge.department"].create({"name": "Dept B"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "Policy"})

        base_user_group = cls.env.ref("base.group_user")
        contributor_group = cls.env.ref(
            "autoinfo_company_knowledge_platform.group_knowledge_contributor"
        )
        reviewer_group = cls.env.ref(
            "autoinfo_company_knowledge_platform.group_knowledge_reviewer"
        )
        manager_group = cls.env.ref(
            "autoinfo_company_knowledge_platform.group_department_manager"
        )
        admin_group = cls.env.ref(
            "autoinfo_company_knowledge_platform.group_knowledge_admin"
        )

        cls.user_contributor_a = cls.env["res.users"].create(
            {
                "name": "Contributor A",
                "login": "write_contributor_a",
                "groups_id": [(6, 0, [base_user_group.id, contributor_group.id])],
                "knowledge_department_id": cls.dept_a.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_contributor_b = cls.env["res.users"].create(
            {
                "name": "Contributor B",
                "login": "write_contributor_b",
                "groups_id": [(6, 0, [base_user_group.id, contributor_group.id])],
                "knowledge_department_id": cls.dept_a.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_reviewer_a = cls.env["res.users"].create(
            {
                "name": "Reviewer A",
                "login": "write_reviewer_a",
                "groups_id": [(6, 0, [base_user_group.id, reviewer_group.id])],
                "knowledge_department_id": cls.dept_a.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_reviewer_b = cls.env["res.users"].create(
            {
                "name": "Reviewer B",
                "login": "write_reviewer_b",
                "groups_id": [(6, 0, [base_user_group.id, reviewer_group.id])],
                "knowledge_department_id": cls.dept_b.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_manager_a = cls.env["res.users"].create(
            {
                "name": "Manager A",
                "login": "write_manager_a",
                "groups_id": [(6, 0, [base_user_group.id, manager_group.id])],
                "knowledge_department_id": cls.dept_a.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_admin = cls.env["res.users"].create(
            {
                "name": "Knowledge Admin",
                "login": "write_admin",
                "groups_id": [(6, 0, [base_user_group.id, admin_group.id])],
                "knowledge_department_id": cls.dept_b.id,
                "knowledge_clearance_level": "internal",
            }
        )

    def _create_draft_item(self, owner):
        return (
            self.env["knowledge.item"]
            .with_user(owner)
            .create(
                {
                    "title": "Draft",
                    "summary": "Draft summary",
                    "body": "<p>Draft</p>",
                    "department_id": self.dept_a.id,
                    "knowledge_type_id": self.knowledge_type.id,
                    "classification": "internal",
                }
            )
        )

    def test_contributor_can_edit_only_own_draft(self):
        item = self._create_draft_item(self.user_contributor_a)
        item.with_user(self.user_contributor_a).write({"summary": "Updated"})
        self.assertEqual(item.summary, "Updated")

        with self.assertRaises(AccessError):
            item.with_user(self.user_contributor_b).write({"summary": "Hack"})

        item.with_user(self.user_contributor_a).action_submit_review()
        with self.assertRaises(AccessError):
            item.with_user(self.user_contributor_a).write({"summary": "Should fail"})

    def test_reviewer_and_manager_can_edit_only_own_department(self):
        item = self._create_draft_item(self.user_contributor_a)
        item.with_user(self.user_contributor_a).action_submit_review()

        item.with_user(self.user_reviewer_a).write({"summary": "Reviewer edit"})
        self.assertEqual(item.summary, "Reviewer edit")

        item.with_user(self.user_manager_a).write({"summary": "Manager edit"})
        self.assertEqual(item.summary, "Manager edit")

        with self.assertRaises(AccessError):
            item.with_user(self.user_reviewer_b).write({"summary": "Other dept edit"})

    def test_no_one_can_change_state_via_write(self):
        item = self._create_draft_item(self.user_contributor_a)
        with self.assertRaises(AccessError):
            item.with_user(self.user_reviewer_a).write({"state": "in_review"})

        item.with_user(self.user_contributor_a).action_submit_review()
        with self.assertRaises(AccessError):
            item.with_user(self.user_reviewer_a).write({"state": "published"})

    def test_no_direct_edit_published(self):
        item = self._create_draft_item(self.user_contributor_a)
        item.with_user(self.user_contributor_a).action_submit_review()
        item.with_user(self.user_reviewer_a).action_publish(change_summary="Publish")
        self.assertEqual(item.state, "published")

        with self.assertRaises(AccessError):
            item.with_user(self.user_reviewer_a).write({"summary": "Edit published"})

        with self.assertRaises(AccessError):
            item.with_user(self.user_admin).write({"summary": "Admin edit published"})
