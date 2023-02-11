class QCluster:
    q_cluster = None

    def __init__(self):
        from django_q.cluster import Cluster

        self.q_cluster = Cluster()
        self.q_cluster.start()
        self.__start_jobs()

    def __start_jobs(self):
        from django.conf import settings
        from django_q.models import Schedule
        from django.utils import timezone
        Schedule.objects.update_or_create(
            func="apps.scheduler.jobs.Jobs.job_temp_task",
            name="job_temp_task",
            defaults={
                "schedule_type": Schedule.CRON,
                "cron": "0 7 * * *",
                "cluster": settings.Q_CLUSTER_CONFIG_NAME,
                "next_run": timezone.now(),
                "repeats": -1,
            },
        )

    def stop(self):
        try:
            self.q_cluster.stop()
        except Exception as e:
            print(e)
