OPERATOR_IMAGE:=docker-registry.default.svc:5000/artifactory-operator/artifactory-operator:latest
PULL_POLICY:=Always

.PHONY: deploy_operator deploy_build
deploy_operator:
	@kubectl apply -f operator/service_account.yaml
	@kubectl apply -f operator/rbac/role.yaml
	@kubectl apply -f operator/rbac/role_binding.yaml
	@kubectl apply -f operator/rbac/cluster_role.yaml
	@kubectl apply -f operator/rbac/cluster_role_binding.yaml
#	@cat operator/deployment.yaml | sed 's|<<<OPERATOR_IMAGE>>>|${OPERATOR_IMAGE}|g; s|<<<PULL_POLICY>>>|${PULL_POLICY}|g;' | kubectl apply -f-

# deploy_build_oc:
# 	@oc apply -f deploy/build_oc/image_stream.yaml
# 	@oc apply -f deploy/build_oc/build_config.yaml

# rebuild_oc:
# 	@oc start-build artifactory-operator -w
# 	@oc delete pod -l name=artifactory-operator --force --grace-period=0
