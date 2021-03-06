from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views.generic import ListView, DetailView

from core.models import Node
from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from core.models import VirtualMachine

from core.models import User

from core.admin import UserCreateForm

from webui.forms.node_os_install_form import NodeOsInstallForm
from webui.forms.node_kvm_create import NodeKvmCreateForm

from webui.forms.virtual_machine_create import VirtualMachineCreateForm

from webui.forms.node_power_off import NodePowerOffForm
from webui.forms.node_power_on import NodePowerOnForm
from webui.forms.node_power_restart import NodePowerRestartForm

from webui.forms.node_docker_create import NodeDockerCreateForm

from core.models import Container

from webui.forms.container_create import ContainerCreateForm

from webui.forms.vm_power_off import VirtualMachinePowerOffForm
from webui.forms.vm_power_on import VirtualMachinePowerOnForm
from webui.forms.vm_power_restart import VirtualMachinePowerRestartForm


def login(request):
    return render(request, 'tala/auth/login.html')


@login_required
def logout(request):
    return render(request, 'tala/auth/logout.html')


@login_required
def index(request):
    context = {'node_count': Node.objects.all().count(), 'vm_count': VirtualMachine.objects.all().count(), 'container_count': Container.objects.all().count()}
    return render(request, 'tala/index.html', context)


def test(request):
    return render(request, 'test/index.html')


def image(request):
    return render(request, 'images/index.html')


class IndexView(LoginRequiredMixin, ListView):
    model = Node
    template_name = 'tala/index.html'


class NodesView(LoginRequiredMixin, ListView):
    model = Node
    template_name = 'tala/nodes/index.html'


class NodeView(LoginRequiredMixin, DetailView):
    model = Node
    template_name = 'tala/nodes/detail.html'


class VirtualMachinesView(LoginRequiredMixin, ListView):
    model = VirtualMachine
    template_name = 'tala/virtual_machines/index.html'


class VirtualMachineView(LoginRequiredMixin, DetailView):
    model = VirtualMachine
    template_name = 'tala/virtual_machines/detail.html'


class ContainersView(LoginRequiredMixin, ListView):
    model = Container
    template_name = 'tala/containers/index.html'


class ContainerView(LoginRequiredMixin, DetailView):
    model = Container
    template_name = 'tala/containers/detail.html'


class UsersView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'tala/users/index.html'


class UserView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'tala/users/detail.html'


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_data(self):
        """Return 3 datasets to plot."""

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]

#line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView, CreateView
from django.shortcuts import render


class NodeOSInstall(CreateView):
    model = Node
    fields = '__all__'

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'news/news_create_success.html', {'news': self.object})


class UserUpdate(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'ssh_public_key']
    template_name = 'tala/users/edit.html'
    success_url = "/ui/users/"


class UserCreate(CreateView):
    form_class = UserCreateForm
    template_name = 'tala/users/create.html'
    success_url = "/ui/users/"


class NodeCreate(CreateView):
    model = Node
    fields = ['name', 'description', 'hostname', 'ipmi_ip_address', 'ipmi_mac_address', 'ipmi_user_name', 'ipmi_password', ]
    template_name = 'tala/nodes/create.html'
    success_url = "/ui/nodes/"

    def form_valid(self, form):
        self.object = form.save()
        self.object.type = "Baremetal"
        self.object.save()
        self.object.vnc_port = 11000 + self.object.id
        self.object.save()
        # ベアメタルの情報を取得
        from core.utils.executor import get_bare_metal_info
        get_bare_metal_info.delay(self.object.id)
        return HttpResponseRedirect('/ui/nodes/')


class NodeUpdate(UpdateView):
    model = Node
    fields = ['name', 'description', 'hostname', 'ipmi_ip_address', 'ipmi_mac_address', 'ipmi_user_name', 'ipmi_password']
    template_name = 'tala/nodes/edit.html'
    success_url = "/ui/nodes/"


class NodeDelete(DeleteView):
    model = Node
    template_name = 'tala/nodes/delete.html'
    success_url = '/ui/nodes/'


class VirtualMachineDelete(DeleteView):
    model = VirtualMachine
    template_name = 'tala/virtual_machines/delete.html'
    success_url = '/ui/virtualmachines/'


class UserDelete(DeleteView):
    model = User
    template_name = 'tala/nodes/delete.html'
    success_url = '/ui/users/'


class NodeOsInstall(FormView):
    template_name = 'tala/nodes/os_install_form.html'
    form_class = NodeOsInstallForm
    success_url = "/ui/nodes/"

    def form_valid(self, form):
        from core.utils.executor import create_bare_metal
        create_bare_metal.delay(self.kwargs['pk'], form.data['os'], form.data['username'])
        node = Node.objects.get(id=self.kwargs['pk'])
        node.os = form.data['os']
        node.password = form.data['password']
        node.save()
        return HttpResponseRedirect('/ui/nodes/')


class NodeKvmCreate(FormView):
    template_name = 'tala/nodes/kvm_create.html'
    form_class = NodeKvmCreateForm
    success_url = "/ui/nodes/"

    def form_valid(self, form):
        from core.utils.executor import create_kvm_hyper_visor
        create_kvm_hyper_visor.delay(self.kwargs['pk'])
        return HttpResponseRedirect('/ui/nodes/')


class NodeDockerCreate(FormView):
    template_name = 'tala/nodes/docker_create.html'
    form_class = NodeDockerCreateForm
    success_url = "/ui/nodes/"

    def form_valid(self, form):
        from core.utils.executor import create_docker
        create_docker.delay(self.kwargs['pk'])
        return HttpResponseRedirect('/ui/nodes/')


class VirtualMachineCreateView(CreateView):
    form_class = VirtualMachineCreateForm
    template_name = 'tala/virtual_machines/create.html'
    success_url = "/ui/virtualmachines/"

    def form_valid(self, form):
        self.object = form.save()
        vm = self.object
        vm.os = form.data['os']
        vm.password = form.data['password']
        vm.save()
        vm.vnc_port = 10000 + vm.id
        vm.save()
        from core.utils.executor import create_virtual_machine
        create_virtual_machine.delay(vm.id)
        return HttpResponseRedirect('/ui/virtualmachines/')


class NodePowerRestart(FormView):
    template_name = 'tala/nodes/node_power_restart.html'
    form_class = NodePowerRestartForm
    success_url = "/ui/nodes/"

    def form_valid(self, form):
        from core.utils.executor import power_control_for_node
        power_control_for_node.delay(self.kwargs['pk'], "restart")
        return HttpResponseRedirect('/ui/nodes/')


class NodePowerOn(FormView):
    template_name = 'tala/nodes/node_power_on.html'
    form_class = NodePowerOnForm
    success_url = "/ui/nodes/"

    def form_valid(self, form):
        from core.utils.executor import power_control_for_node
        power_control_for_node.delay(self.kwargs['pk'], "on")
        return HttpResponseRedirect('/ui/nodes/')


class NodePowerOff(FormView):
    template_name = 'tala/nodes/node_power_off.html'
    form_class = NodePowerOffForm
    success_url = "/ui/nodes/"

    def form_valid(self, form):
        from core.utils.executor import power_control_for_node
        power_control_for_node.delay(self.kwargs['pk'], "off")
        return HttpResponseRedirect('/ui/nodes/')


class ContainersCreateView(CreateView):
    form_class = ContainerCreateForm
    template_name = 'tala/containers/create.html'
    success_url = "/ui/containers/"

    def form_valid(self, form):
        # TODO: コンテナ作成処理を作る
        #from core.utils.executor import create_bare_metal
        #create_bare_metal.delay(self.kwargs['pk'], form.data['os'], form.data['username'])
        self.object = form.save()
        return HttpResponseRedirect('/ui/containers/')


class VirtualMachineUpdate(UpdateView):
    model = VirtualMachine
    fields = ['name', 'description']
    template_name = 'tala/virtual_machines/edit.html'
    success_url = "/ui/virtualmachines/"


class ContainerUpdate(UpdateView):
    model = Container
    fields = ['name', 'description']
    template_name = 'tala/containers/edit.html'
    success_url = "/ui/containers/"


class ContainerDelete(DeleteView):
    model = Container
    template_name = 'tala/containers/delete.html'
    success_url = '/ui/containers/'


class VirtualMachinePowerRestart(FormView):
    template_name = 'tala/virtual_machines/vm_power_restart.html'
    form_class = VirtualMachinePowerRestartForm
    success_url = "/ui/virtualmachines/"

    def form_valid(self, form):
        from core.utils.executor import power_control_for_vm
        power_control_for_vm.delay(self.kwargs['pk'], "restart")
        return HttpResponseRedirect('/ui/virtualmachines/')


class VirtualMachinePowerOn(FormView):
    template_name = 'tala/virtual_machines/vm_power_on.html'
    form_class = VirtualMachinePowerOnForm
    success_url = "/ui/virtualmachines/"

    def form_valid(self, form):
        from core.utils.executor import power_control_for_vm
        power_control_for_vm.delay(self.kwargs['pk'], "on")
        return HttpResponseRedirect('/ui/virtualmachines/')


class VirtualMachinePowerOff(FormView):
    template_name = 'tala/virtual_machines/vm_power_off.html'
    form_class = VirtualMachinePowerOffForm
    success_url = "/ui/virtualmachines/"

    def form_valid(self, form):
        from core.utils.executor import power_control_for_vm
        power_control_for_vm.delay(self.kwargs['pk'], "off")
        return HttpResponseRedirect('/ui/virtualmachines/')
