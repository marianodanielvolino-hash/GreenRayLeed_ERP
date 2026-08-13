ARG ERPNEXT_VERSION=v16.32.0
FROM frappe/erpnext:${ERPNEXT_VERSION}

USER root
COPY --chown=frappe:frappe fch_ops /home/frappe/frappe-bench/apps/fch_ops

USER frappe
RUN /home/frappe/frappe-bench/env/bin/pip install --no-cache-dir -e /home/frappe/frappe-bench/apps/fch_ops \
    && mkdir -p /home/frappe/frappe-bench/assets/fch_ops \
    && cp -a /home/frappe/frappe-bench/apps/fch_ops/fch_ops/public/. /home/frappe/frappe-bench/assets/fch_ops/

WORKDIR /home/frappe/frappe-bench
