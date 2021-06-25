import itk
import vtk

def checkAbort(obj, event):
    if obj.GetEventPending() != 0:
        obj.SetAbortRender(1)

def generate_output(input_filename):
    input_image = itk.imread(input_filename)
    dimension = input_image.GetImageDimension()

    InputImageType = itk.Image[itk.SS, dimension]
    OutputImageType = itk.Image[itk.UC, dimension]

    threshold_image_filter = itk.ConnectedThresholdImageFilter[InputImageType, InputImageType].New(input_image)
    threshold_image_filter.SetLower(180)
    threshold_image_filter.SetUpper(400)
    threshold_image_filter.AddSeed([410, 320, 70])
    threshold_image_filter.AddSeed([130, 240, 30])
    threshold_image_filter.Update()

    threshold_image_output = threshold_image_filter.GetOutput()

    rescale_image_filter = itk.RescaleIntensityImageFilter[InputImageType, OutputImageType].New(threshold_image_output)
    rescale_image_filter.Update()

    return rescale_image_filter

if __name__ == '__main__':
    input_filename = 'abdomen.mha'
    output_filename = 'output.mha'

    output = generate_output(input_filename)
    itk.imwrite(output, output_filename)

    #########
    # INPUT #
    #########

    # reader input
    reader_input = vtk.vtkMetaImageReader()
    reader_input.SetFileName(input_filename)

    # volume mapper input
    volume_mapper_input = vtk.vtkSmartVolumeMapper()
    volume_mapper_input.SetInputConnection(reader_input.GetOutputPort())

    # opacity func input
    opacity_func_input = vtk.vtkPiecewiseFunction()
    opacity_func_input.AddPoint(80, 0)
    opacity_func_input.AddPoint(255, 0.3)

    # volume property input
    volume_property_input = vtk.vtkVolumeProperty()
    volume_property_input.SetScalarOpacity(opacity_func_input)

    # volume input
    volume_input = vtk.vtkVolume()
    volume_input.SetMapper(volume_mapper_input)
    volume_input.SetProperty(volume_property_input)

    ##########
    # OUTPUT #
    ##########

    # reader output
    reader_output = vtk.vtkMetaImageReader()
    reader_output.SetFileName(output_filename)

    # volume mapper ouput
    volume_mapper_output = vtk.vtkSmartVolumeMapper()
    volume_mapper_output.SetInputConnection(reader_output.GetOutputPort())

    # opacity func output
    opacity_func_output = vtk.vtkPiecewiseFunction()
    opacity_func_output.AddPoint(250, 0)
    opacity_func_output.AddPoint(255, 0.3)

    # color func output
    color_func_output = vtk.vtkColorTransferFunction()
    color_func_output.AddRGBPoint(250, 0, 0, 0)
    color_func_output.AddRGBPoint(255, 0, 0, 1)

    # volume property output
    volume_property_output = vtk.vtkVolumeProperty()
    volume_property_output.SetColor(color_func_output)
    volume_property_output.SetScalarOpacity(opacity_func_output)

    # volume output
    volume_output = vtk.vtkVolume()
    volume_output.SetMapper(volume_mapper_output)
    volume_output.SetProperty(volume_property_output)

    # renderer
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(1, 1, 1)

    renderer.AddActor(volume_input)
    renderer.AddActor(volume_output)

    # window
    window = vtk.vtkRenderWindow()
    window.AddRenderer(renderer)
    window.AddObserver("AbortCheckEvent", checkAbort)

    # window intereractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(window)

    # Let's render baby
    iren.Initialize()
    window.Render()
    iren.Start()
