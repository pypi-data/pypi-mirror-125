from selenium.webdriver.common.by import By

from sop import DEFAULT_TIMOUT_ACTION
from sop.odoo.dialogs import MailComposeForm, RegisterPayementWizardForm
from sop.odoo.views import FormViewMixin, ListViewMixin, OdooBasePage


class BaseAccountingPageLocators:
    PAGE_SELECTOR = (By.XPATH, "//nav//a[contains(text(), 'Facturation')]")

    MAIN_MENU_CUSTOMER = (
        By.CSS_SELECTOR,
        "a[data-menu-xmlid='account.menu_finance_receivables']",
    )
    MENU_INVOICE = (
        By.CSS_SELECTOR,
        "a[data-menu-xmlid='account.menu_action_move_out_invoice_type']",
    )


class BaseAccountingPage(OdooBasePage):
    _page_selector = BaseAccountingPageLocators.PAGE_SELECTOR

    def click_menu_invoice(self) -> "InvoiceListViewPage":
        """Overwrite OdooBasePage"""
        self.click(BaseAccountingPageLocators.MAIN_MENU_CUSTOMER)
        self.click(BaseAccountingPageLocators.MENU_INVOICE)
        return InvoiceListViewPage(self.driver)


class InvoiceFormViewPageLocators:
    PAGE_SELECTOR = (By.CSS_SELECTOR, "div.o_form_view")
    CONFIRM = (
        By.XPATH,
        '//button[@name="action_post"]/span[contains(text(), "Confirmer")]',
    )
    REGISTER_PAYMENT = (By.NAME, "action_register_payment")


class InvoiceFormViewPage(BaseAccountingPage, MailComposeForm, FormViewMixin):
    _page_selector = InvoiceFormViewPageLocators.PAGE_SELECTOR

    def confirm(self, timeout=DEFAULT_TIMOUT_ACTION):
        self.click(InvoiceFormViewPageLocators.CONFIRM, timeout=timeout)

    def register_payement(self, timeout=DEFAULT_TIMOUT_ACTION):
        self.click(InvoiceFormViewPageLocators.REGISTER_PAYMENT, timeout=timeout)
        return RegisterPayementWizardForm(self.driver, timeout=timeout)


class InvoiceListViewPageLocators:
    PAGE_SELECTOR = (By.CSS_SELECTOR, "div.o_list_view")


class InvoiceListViewPage(BaseAccountingPage, ListViewMixin):
    _page_selector = InvoiceListViewPageLocators.PAGE_SELECTOR
    _form_view = InvoiceFormViewPage
