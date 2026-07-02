from odoo.exceptions import AccessError
from odoo.tests.common import SavepointCase


class TestKnowledgePublishPermissions(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.dept_a = cls.env["knowledge.department"].create({"name": "Dept A"})
        cls.dept_b = cls.env["knowledge.department"].create({"name": "Dept B"})
        cls.knowledge_type = cls.env["knowledge.type"].create({"name": "SOP"})

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
                "login": "contributor_a",
                "groups_id": [(6, 0, [base_user_group.id, contributor_group.id])],
                "knowledge_department_id": cls.dept_a.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_reviewer_a = cls.env["res.users"].create(
            {
                "name": "Reviewer A",
                "login": "reviewer_a",
                "groups_id": [(6, 0, [base_user_group.id, reviewer_group.id])],
                "knowledge_department_id": cls.dept_a.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_reviewer_b = cls.env["res.users"].create(
            {
                "name": "Reviewer B",
                "login": "reviewer_b",
                "groups_id": [(6, 0, [base_user_group.id, reviewer_group.id])],
                "knowledge_department_id": cls.dept_b.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_manager_a = cls.env["res.users"].create(
            {
                "name": "Manager A",
                "login": "manager_a",
                "groups_id": [(6, 0, [base_user_group.id, manager_group.id])],
                "knowledge_department_id": cls.dept_a.id,
                "knowledge_clearance_level": "internal",
            }
        )
        cls.user_admin_b = cls.env["res.users"].create(
            {
                "name": "Admin B",
                "login": "admin_b",
                "groups_id": [(6, 0, [base_user_group.id, admin_group.id])],
                "knowledge_department_id": cls.dept_b.id,
                "knowledge_clearance_level": "internal",
            }
        )

    def _create_item(self):
        item = self.env["knowledge.item"].create(
            {
                "title": "Dept A SOP",
                "summary": "Draft SOP",
                "department_id": self.dept_a.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
                "body": "<p>Draft</p>",
            }
        )
        item.action_submit_review()
        return item

    def _create_draft_item(self):
        return self.env["knowledge.item"].create(
            {
                "title": "Dept A Draft SOP",
                "summary": "Draft SOP",
                "department_id": self.dept_a.id,
                "knowledge_type_id": self.knowledge_type.id,
                "classification": "internal",
                "body": "<p>Draft</p>",
            }
        )

    def test_contributor_cannot_publish(self):
        item = self._create_item()
        with self.assertRaises(AccessError):
            item.with_user(self.user_contributor_a).action_publish(
                change_summary="Try publish"
            )

    def test_reviewer_can_publish_only_own_department(self):
        item = self._create_item()
        with self.assertRaises(AccessError):
            item.with_user(self.user_reviewer_b).action_publish(
                change_summary="Wrong dept"
            )

        item.with_user(self.user_reviewer_a).action_publish(change_summary="OK")
        self.assertEqual(item.state, "published")

    def test_reviewer_cannot_publish_when_not_in_review(self):
        item = self._create_draft_item()
        with self.assertRaises(AccessError):
            item.with_user(self.user_reviewer_a).action_publish(change_summary="No")

    def test_manager_can_publish_only_own_department(self):
        item = self._create_item()
        item.with_user(self.user_manager_a).action_publish(change_summary="OK")
        self.assertEqual(item.state, "published")

    def test_manager_cannot_publish_when_not_in_review(self):
        item = self._create_draft_item()
        with self.assertRaises(AccessError):
            item.with_user(self.user_manager_a).action_publish(change_summary="No")

    def test_admin_can_publish_all_departments(self):
        item = self._create_item()
        item.with_user(self.user_admin_b).action_publish(change_summary="OK")
        self.assertEqual(item.state, "published")

    def test_admin_can_publish_when_not_in_review(self):
        item = self._create_draft_item()
        item.with_user(self.user_admin_b).action_publish(change_summary="OK")
        self.assertEqual(item.state, "published")
