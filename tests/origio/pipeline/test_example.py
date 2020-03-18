from origo.pipelines.client import PipelineApiClient
from origo.pipelines.resources.pipeline import Pipeline
from origo.pipelines.resources.pipeline_instance import PipelineInstance


def test_resource_example(
    mock_get_pipeline_instance,
    mock_get_pipeline,
    mock_list_instances,
    mock_create_pipeline_instance,
):
    print("Getting pipeline")
    sdk = PipelineApiClient()
    test_excel_to_csv: Pipeline = sdk.fetch(
        Pipeline,
        "arn:aws:states:eu-west-1:123456789101:stateMachine:test-pipeline-excel-to-csv",
    )
    assert mock_get_pipeline.called

    print("Valiate pipeline: ", end="")
    valid, _ = test_excel_to_csv.validate()
    print(valid)
    assert valid

    print("List instances for pipeline: ", end="")
    instances, error = test_excel_to_csv.list_instances()
    print(instances)
    assert mock_list_instances.called

    test_excel_to_csv.transformation_schema = 12314
    valid, errors = test_excel_to_csv.validate()
    if errors:
        assert errors.message == "12314 is not of type 'string'"

    instance: PipelineInstance = instances[0]
    instance.schemaId = "blabla"
    instance.create()

    assert mock_create_pipeline_instance.called


def test_bootstrap_script(
    mock_get_pipeline_instance,
    mock_create_pipeline,
    mock_list_instances,
    mock_create_pipeline_instance,
):
    sdk = PipelineApiClient()

    pipeline = Pipeline(
        sdk,
        "arn:aws:states:eu-west-1:123456789101:stateMachine:blablabla",
        "template goes here",
        "some transformation schema",
    )
    pipeline.create()

    instance = PipelineInstance(
        sdk,
        id="uuid?",
        datasetUri="boligpriser",
        schemaId="coming soon",
        taskConfig="transformation goes here",
        pipelineArn=pipeline.arn,
        useLatestEdition=True,
    )
    valid, error = instance.validate()
    assert not valid
    assert error.message.startswith("'boligpriser' does not match ")
    instance.datasetUri = "output/boligpriser/1"
    instance.transformation = {"transformation": "goes here"}
    instance.create()
    assert mock_create_pipeline_instance.called
